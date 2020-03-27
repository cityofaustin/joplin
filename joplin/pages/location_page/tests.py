import pytest

from importer.page_importer import PageImporter
from pages.location_page.models import LocationPage
import pages.location_page.fixtures as fixtures
import pages.location_page.fixtures.helpers.components as components


@pytest.mark.django_db
def test_create_location_page_from_api(remote_staging_preview_url, remote_pytest_api):
    url = f'{remote_staging_preview_url}/location/UGFnZVJldmlzaW9uTm9kZTozMzc3?CMS_API={remote_pytest_api}'
    page = PageImporter(url).fetch_page_data().create_page()
    assert isinstance(page, LocationPage)


@pytest.mark.django_db
def test_create_location_page_with_title():
    page = fixtures.title()
    assert isinstance(page, LocationPage)
    assert page.title == "Location Page with title"
    assert page.slug == "location-page-with-title"
