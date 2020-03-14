from urllib.parse import urlparse
from pathlib import Path
from gql import gql, Client
from gql.transport.requests import RequestsHTTPTransport

query = gql('''
{
	allDepartmentPages {
    edges {
      node {
        topPages {
          edges {
            node {
              title
              slug
              department {
                slug
              }
            }
          }
        }
      }
    }
  }
}
''')


ENDPOINTS = {
    'janis.austintexas.io': 'https://joplin-staging.herokuapp.com/api/graphql'
}


class PageImporter:

    def query_page_with_graphql(self):
        sample_transport = RequestsHTTPTransport(
            url=self.joplin_api_endpoint,
            # use_json=True,
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

        result = client.execute(query)
        blarg = 3

    def parse_janis_preview_url(self, path):
        # for now, just assuming these parts are always right
        self.language = path.parts[1]
        self.page_type = path.parts[3]
        self.revision_id = path.parts[4]

    def parse_url(self):
        # get a urllib.parse result to play with
        parse_result = urlparse(self.url_to_parse)

        # get a joplin api endpoint
        if parse_result.hostname in ENDPOINTS:
            self.joplin_api_endpoint = ENDPOINTS[parse_result.hostname]

        # get a path object to play with
        path = Path(parse_result.path)

        # figure out if we're a janis preview url
        if 'preview' in path.parts:
            self.parse_janis_preview_url(path)

    def __init__(self, url):
        self.url_to_parse = url
        self.joplin_api_endpoint = ''
        self.language = ''
        self.page_type = ''
        self.revision_id = ''
        self.parse_url()
