from urllib.parse import urlparse, parse_qs
from pathlib import Path
from gql import Client
from gql.transport.requests import RequestsHTTPTransport
import json
from django.core.exceptions import ValidationError
from humps import decamelize

from importer.queries import queries
from importer.create_from_importer import create_page_from_importer

# TODO: this could be retrieved programmatically from the netlify API for PR apps
ENDPOINTS = {
    'janis.austintexas.io': 'https://joplin-staging.herokuapp.com/api/graphql',
    'janis-pytest.netlify.com': 'https://joplin-pr-pytest.herokuapp.com/api/graphql',
}


def change_keys(obj, convert):
    """
    Recursively goes through the dictionary obj and replaces keys with the convert function.
    """
    if isinstance(obj, (str, int, float)):
        return obj
    if isinstance(obj, dict):
        new = obj.__class__()
        for k, v in obj.items():
            new[convert(k)] = change_keys(v, convert)
    elif isinstance(obj, (list, set, tuple)):
        new = obj.__class__(change_keys(v, convert) for v in obj)
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
        cleaned_page_dictionary = change_keys(cleaned_page_dictionary, fix_nums)

        return cleaned_page_dictionary


    def fetch_page_data(self):
        # todo: don't just hardcode lang here
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
            revision_node = result['allPageRevisions']['edges'][0]['node']

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
