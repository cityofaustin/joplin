import pytest

from importer.page_importer import PageImporter
from pages.service_page.models import ServicePage


@pytest.mark.django_db
def test_create_service_page_from_api(remote_staging_preview_url, remote_pytest_api):
    url = f'{remote_staging_preview_url}/services/UGFnZVJldmlzaW9uTm9kZToyMQ==?CMS_API={remote_pytest_api}'
    page = PageImporter(url).fetch_page_data().create_page()
    assert isinstance(page, ServicePage)
