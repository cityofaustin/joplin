from urllib.parse import urlparse, parse_qs
from pathlib import Path
from gql import gql, Client
from gql.transport.requests import RequestsHTTPTransport
import json
from django.core.exceptions import ValidationError
from humps import decamelize

from importer.queries import queries
from pages.topic_collection_page.factories import create_topic_collection_page_from_importer_dictionaries
from pages.topic_page.factories import create_topic_page_from_importer_dictionaries
from pages.information_page.factories import create_information_page_from_importer_dictionaries
from pages.service_page.factories import create_service_page_from_page_dictionary

# TODO: this could be retrieved programmatically from the netlify API for PR apps
ENDPOINTS = {
    'janis.austintexas.io': 'https://joplin-staging.herokuapp.com/api/graphql',
    'janis-pytest.netlify.com': 'https://joplin-pr-pytest.herokuapp.com/api/graphql',
}


class PageImporter:
    def create_page(self):
        page_creators = {
            'topiccollection': create_topic_collection_page_from_importer_dictionaries,
            'topic': create_topic_page_from_importer_dictionaries,
            'information': create_information_page_from_importer_dictionaries,
            'services': create_service_page_from_page_dictionary,
        }

        page = page_creators[self.page_type](self.page_dictionaries, self.revision_id)

        return page

    def fetch_page_data(self):
        # todo: don't just hardcode lang here
        for lang in ['en', 'es']:
            sample_transport = RequestsHTTPTransport(
                url=self.joplin_api_endpoint,
                headers={'Accept-Language': lang},
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

            # set the deCamelCased page dictionary for this lang
            self.page_dictionaries[lang] = decamelize(page_dictionary_from_revision)

        # return ourselves for method chaining
        return self

    def __init__(self, url):
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

        self.page_dictionaries = {}
