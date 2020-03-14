from urllib.parse import urlparse
from pathlib import Path

ENDPOINTS = {
    'janis.austintexas.io': 'https://joplin-staging.herokuapp.com/api/graphql'
}


class PageImporter:
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
