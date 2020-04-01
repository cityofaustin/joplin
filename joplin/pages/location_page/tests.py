import pytest

from importer.page_importer import PageImporter
from pages.location_page.models import LocationPage
import pages.location_page.fixtures as fixtures
from pages.location_page.factories import LocationPageFactory


@pytest.mark.django_db
def test_create_location_page_from_api(remote_staging_preview_url, remote_pytest_api):
    url = f'{remote_staging_preview_url}/location/UGFnZVJldmlzaW9uTm9kZTozMA==?CMS_API={remote_pytest_api}'
    page = PageImporter(url).fetch_page_data().create_page()
    assert isinstance(page, LocationPage)


@pytest.mark.django_db
def test_create_location_page_with_title():
    page = fixtures.title()
    assert isinstance(page, LocationPage)
    assert page.title == "Location page with title"
    assert page.slug == "location-page-with-title"


# If location page is live
# and coa_global=False (top level is not checked)
@pytest.mark.django_db
def test_location_page_with_urls():
    janis_url_page_type = 'location'

    page = LocationPageFactory.create(
        slug="page_slug",
        coa_global=False,
    )

    # Set expected urls using janis url page type and location page slugs
    expected_urls = ['http://fake.base.url/{page_type}/{page_slug}'.format(
                            page_type=janis_url_page_type,
                            page_slug=page.slug)]

    urls = page.janis_urls()
    url = page.janis_url()

    # we should get a url under every location
    assert urls == expected_urls
    assert url == expected_urls[0]
