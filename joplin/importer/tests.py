import pytest
from importer.page_importer import PageImporter

def test__parse_janis_preview_url():
    preview_url = 'https://janis.austintexas.io/en/preview/information/UGFnZVJldmlzaW9uTm9kZToyNjI4'

    page_importer = PageImporter(preview_url)

    assert page_importer.url_to_parse == preview_url
    assert page_importer.joplin_api_endpoint == 'https://joplin-staging.herokuapp.com/api/graphql'
    assert page_importer.language == 'en'
    assert page_importer.page_type == 'information'
    assert page_importer.revision_id == 'UGFnZVJldmlzaW9uTm9kZToyNjI4'
