import pytest
from importer.page_importer import PageImporter

def test_parse_janis_preview_url():
    preview_url = 'https://janis.austintexas.io/en/preview/information/UGFnZVJldmlzaW9uTm9kZToyNjI4'

    page_importer = PageImporter(preview_url)

    assert page_importer.url_to_parse == preview_url
    assert page_importer.joplin_api_endpoint == 'https://joplin-staging.herokuapp.com/api/graphql'
    assert page_importer.language == 'en'
    assert page_importer.page_type == 'information'
    assert page_importer.revision_id == 'UGFnZVJldmlzaW9uTm9kZToyNjI4'

# this test will start breaking once we no longer have this revision in the db
# todo: figure out a good way to mock api responses
def test_import_information_page():
    preview_url = 'https://janis.austintexas.io/en/preview/information/UGFnZVJldmlzaW9uTm9kZToyNjI4'

    page_importer = PageImporter(preview_url)
    page_importer.query_page_with_graphql()
    blarg = 3
