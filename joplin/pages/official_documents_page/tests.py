import pytest

from importer.page_importer import PageImporter
from pages.official_documents_page.models import OfficialDocumentPage
import pages.official_documents_page.fixtures as fixtures

@pytest.mark.django_db
def test_create_official_documents_page_from_api(remote_staging_preview_url, remote_pytest_api):
    url = f'{remote_staging_preview_url}/official_document/UGFnZVJldmlzaW9uTm9kZTozNg==?CMS_API={remote_pytest_api}'
    page = PageImporter(url).fetch_page_data().create_page()
    assert isinstance(page, OfficialDocumentPage)

@pytest.mark.django_db
def test_kitchen_sink():
    page = fixtures.kitchen_sink()
    assert isinstance(page, OfficialDocumentPage)
