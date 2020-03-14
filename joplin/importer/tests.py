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
def test_get_information_page_from_revision():
    preview_url = 'https://janis.austintexas.io/en/preview/information/UGFnZVJldmlzaW9uTm9kZToyNjI4'

    page_importer = PageImporter(preview_url)
    page_dictionary = page_importer.get_page_dictionary_from_revision()

    assert page_dictionary['id'] == 'SW5mb3JtYXRpb25QYWdlTm9kZToxMjM='
    assert page_dictionary['title'] == 'Fire safety checklist for mobile food vendors'
    assert page_dictionary['description'] == 'Any mobile food vendor who uses propane or propane accessories and operates in the City of Austin or Travis County must get a fire safety inspection.'
