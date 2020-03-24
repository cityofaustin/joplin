from urllib.parse import urlparse, parse_qs
from pathlib import Path
from gql import gql, Client
from gql.transport.requests import RequestsHTTPTransport
import json
from importer.queries import queries

from pages.topic_collection_page.factories import create_topic_collection_page_from_page_dictionary
from pages.topic_page.factories import create_topic_page_from_page_dictionary
from pages.information_page.factories import create_information_page_from_page_dictionary
from pages.service_page.factories import create_service_page_from_page_dictionary

ENDPOINTS = {
    'janis.austintexas.io': 'https://joplin-staging.herokuapp.com/api/graphql'
}


class PageImporter:
    def create_page(self):
        page_creator_dictionary = {
            'topiccollection': create_topic_collection_page_from_page_dictionary,
            'topic': create_topic_page_from_page_dictionary,
            'information': create_information_page_from_page_dictionary,
            'services': create_service_page_from_page_dictionary,
        }

        page = page_creator_dictionary[self.page_type](self.page_dictionary, self.revision_id)

        return page

    def fetch_page_data(self):
        sample_transport = RequestsHTTPTransport(
            url=self.joplin_api_endpoint,
            # todo: use headers to get different languages
            # headers={
            #     "Content-type": "application/json",
            # },
            verify=False
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

        # set the page dictionary on ourselves but also return it
        self.page_dictionary = page_dictionary_from_revision

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

        # get a path object to play with
        path = Path(parse_result.path)

        # figure out if we're a janis preview url
        if 'preview' in path.parts:
            # for now, just assuming these parts are always right
            self.language = path.parts[1]
            self.page_type = path.parts[3]
            self.revision_id = path.parts[4]

        self.page_dictionary = None