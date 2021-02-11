import pytest

from importer.page_importer import PageImporter
from pages.location_page.models import LocationPage
import pages.location_page.fixtures as fixtures
from pages.location_page.factories import LocationPageFactory


# @pytest.mark.django_db
@pytest.mark.skip("importer test")
def test_create_location_page_from_api(remote_staging_preview_url, test_api_url, test_api_jwt_token):
    url = f'{remote_staging_preview_url}/location/UGFnZVJldmlzaW9uTm9kZToyNA==?CMS_API={test_api_url}'
    page = PageImporter(url, test_api_jwt_token).fetch_page_data().create_page()
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
def test_location_page_with_urls(home_page, expected_publish_url_base):
    janis_url_page_type = 'location'

    page = LocationPageFactory.create(
        slug="page_slug",
        coa_global=False,
        parent=home_page,
    )

    # Set expected urls using janis url page type and location page slugs
    expected_urls = ['/{page_type}/{page_slug}'.format(
                            page_type=janis_url_page_type,
                            page_slug=page.slug)]

    urls = page.janis_urls()
    janis_publish_url = page.janis_publish_url()

    # we should get a url under every location
    assert urls == expected_urls
    assert janis_publish_url == f'{expected_publish_url_base}{expected_urls[0]}'
