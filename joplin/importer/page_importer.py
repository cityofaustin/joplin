from urllib.parse import urlparse, parse_qs
from pathlib import Path
from gql import Client
from gql.transport.requests import RequestsHTTPTransport
import json
from django.core.exceptions import ValidationError
from humps import decamelize
from bs4 import BeautifulSoup

from importer.queries import queries
from importer.create_from_importer import create_page_from_importer
from pages.home_page.models import HomePage
from pages.base_page.models import JanisBasePage
from pages.service_page.factories import ServicePageFactory

# TODO: this could be retrieved programmatically from the netlify API for PR apps
ENDPOINTS = {
    'alpha.austin.gov': 'https://joplin.herokuapp.com/api/graphql',
    'janis-pytest.netlify.com': 'https://joplin-pr-pytest.herokuapp.com/api/graphql',
    'janis.austintexas.io': 'https://joplin-staging.herokuapp.com/api/graphql',
}


def change_keys(obj, convert, page_dictionary):
    """
    Recursively goes through the dictionary obj and replaces keys with the convert function.
    """
    if isinstance(obj, (int, float)):
        return obj
    if isinstance(obj, str):
        # if our string is html and has links, check for/recreate internal links
        soup = BeautifulSoup(obj, 'html.parser')
        if soup and soup.find('a'):
            # get all the links
            for link in soup.find_all('a'):
                # get a urllib.parse result to play with
                parse_result = urlparse(link.get('href'))

                # check by hostname to see if this isn't an internal link
                if parse_result.hostname not in ENDPOINTS:
                    continue

                # we're dealing with an internal link, let's get the slug
                slug = Path(parse_result.path).parts[-1]

                # first try to get a previously imported page by slug
                try:
                    page = JanisBasePage.objects.get(slug=slug)
                except JanisBasePage.DoesNotExist:
                    page = None

                # if we didn't get a page from the link's slug
                if not page:
                    try:
                        # make sure the page doesn't go live
                        page_dictionary['live'] = False

                        # use a placeholder
                        page = JanisBasePage.objects.get(slug='placeholder_service_page_for_internal_links')
                    except JanisBasePage.DoesNotExist:
                        placeholder_page_dictionary = {
                            'parent': HomePage.objects.first(),
                            'title': 'Placeholder service page for internal links',
                            'slug': 'placeholder_service_page_for_internal_links'
                        }
                        page = ServicePageFactory.create(**placeholder_page_dictionary)

                # the wagtail editor looks for page ids and linktypes when parsing rich text html for internal links
                del link['href']
                link['id'] = page.id
                link['linktype'] = 'page'

            # return our cleaned soup
            return str(soup)
        else:
            return obj
    if isinstance(obj, dict):
        new = obj.__class__()
        for k, v in obj.items():
            new[convert(k)] = change_keys(v, convert, page_dictionary)
    elif isinstance(obj, (list, set, tuple)):
        new = obj.__class__(change_keys(v, convert, page_dictionary) for v in obj)
    else:
        return obj
    return new


class PageImporter:
    def create_page(self):
        return create_page_from_importer(self.page_type, self.page_dictionaries, self.revision_id)

    def __clean_page_data(self, page_dictionary_from_revision):
        # set the deCamelCased page dictionary
        cleaned_page_dictionary = decamelize(page_dictionary_from_revision)

        # Undo some of the changes caused by decamelize
        # time2 and bus2 needs to be bus_2 and time_2
        def fix_nums(k): return k.translate(str.maketrans({'1': '_1', '2': '_2', '3': '_3'}))
        cleaned_page_dictionary = change_keys(cleaned_page_dictionary, fix_nums, cleaned_page_dictionary)

        return cleaned_page_dictionary

    def fetch_page_data(self):
        # Fetches page data in both languages
        for lang in ['en', 'es']:
            sample_transport = RequestsHTTPTransport(
                url=self.joplin_api_endpoint,
                headers={
                    'Accept-Language': lang,
                    'Authorization': f'JWT {self.jwt_token}',
                },
                verify=True
            )

            client = Client(
                retries=3,
                transport=sample_transport,
                fetch_schema_from_transport=True,
            )

            result = client.execute(queries[self.page_type], variable_values=json.dumps({'id': self.revision_id}))
            # revision_node = result['allPageRevisions']['edges'][0]['node']
            revision_node = result['pageRevision']['asGuidePage']

            # this gets us into the 'as____Page' stuff
            page_dictionary_from_revision = next(iter(revision_node.values()))

            self.page_dictionaries[lang] = self.__clean_page_data(page_dictionary_from_revision)

        # return ourselves for method chaining
        return self

    def __init__(self, url, jwt_token):
        # get a urllib.parse result to play with
        parse_result = urlparse(url)

        # get a joplin api endpoint
        if parse_result.hostname in ENDPOINTS:
            self.joplin_api_endpoint = ENDPOINTS[parse_result.hostname]

        if 'CMS_API' in parse_result.query:
            qs = parse_qs(parse_result.query)
            self.joplin_api_endpoint = qs['CMS_API'][0]

        if not hasattr(self, 'joplin_api_endpoint'):
            raise ValidationError(f"hostname [{parse_result.hostname}] does not have a joplin_api_endpoint configured.")

        # get a path object to play with
        path = Path(parse_result.path)

        # figure out if we're a janis preview url
        if 'preview' in path.parts:
            # for now, just assuming these parts are always right
            self.language = path.parts[1]
            self.page_type = path.parts[3]
            self.revision_id = path.parts[4]

        self.jwt_token = jwt_token

        self.page_dictionaries = {}
