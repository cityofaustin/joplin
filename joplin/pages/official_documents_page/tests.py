import pytest

from importer.page_importer import PageImporter
from pages.official_documents_page.models import OfficialDocumentPage
import pages.official_documents_page.fixtures as fixtures

@pytest.mark.django_db
def test_create_official_documents_page_from_api(remote_staging_preview_url, test_api_url, test_api_jwt_token):
    url = f'{remote_staging_preview_url}/official_document/UGFnZVJldmlzaW9uTm9kZToyNQ==?CMS_API={test_api_url}'
    page = PageImporter(url, test_api_jwt_token).fetch_page_data().create_page()
    assert isinstance(page, OfficialDocumentPage)

@pytest.mark.django_db
def test_kitchen_sink():
    page = fixtures.kitchen_sink()
    assert isinstance(page, OfficialDocumentPage)
