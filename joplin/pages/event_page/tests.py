import pytest

from importer.page_importer import PageImporter
from pages.event_page.models import EventPage
import pages.event_page.fixtures as fixtures
from pages.event_page.factories import EventPageFactory
import pages.event_page.fixtures.helpers.components as components


@pytest.mark.django_db
def test_create_event_page_with_title():
    page = fixtures.title()
    assert isinstance(page, EventPage)
    assert page.title == "Event page with title"
    assert page.slug == "Event-page-with-title"


# If Event page has janis url
@pytest.mark.django_db
def test_event_page_with_urls(home_page, expected_publish_url_base):
    janis_url_page_type = 'event'

    page = EventPageFactory.create(
        slug="page_slug",
        coa_global=False,
        parent=home_page,
        date="2020-9-29"
    )

    # Set expected urls using janis url page type and Event page year, month, day and slug
    expected_urls = ['/{page_type}/{page_year}/{page_month}/{page_day}/{page_slug}'.format(
                            page_type=janis_url_page_type,
                            page_year=page.date.year,
                            page_month=page.date.month,
                            page_day=page.date.day,
                            page_slug=page.slug)]

    urls = page.janis_urls()
    janis_publish_url = page.janis_publish_url()

    # we should get a url under every Event
    assert urls == expected_urls
    assert janis_publish_url == f'{expected_publish_url_base}{expected_urls[0]}'


# If Event page has only a title
# it should have no urls
@pytest.mark.django_db
def test_event_page_with_no_urls():
    page = fixtures.title()
    urls = page.janis_urls()
    janis_publish_url = page.janis_publish_url()

    assert urls == []
    assert janis_publish_url == '#'


@pytest.mark.django_db
def test_create_event_page_with_city_location():
    page = fixtures.city_location()
    assert isinstance(page, EventPage)
    assert page.title == "Event at city location"
    assert page.slug == "event-at-city-location"
    # Add autogenerated streamfield "id" to expected value
    expected_location_blocks = components.city_location_block()
    expected_location_blocks[0]["id"] = page.location_blocks.stream_data[0]["id"]
    assert page.location_blocks.stream_data == expected_location_blocks


@pytest.mark.django_db
def test_import_event_page_with_city_location(remote_staging_preview_url, test_api_url, test_api_jwt_token):
    url = f'{remote_staging_preview_url}/event/UGFnZVJldmlzaW9uTm9kZTo0NA==?CMS_API={test_api_url}'
    page = PageImporter(url, test_api_jwt_token).fetch_page_data().create_page()
    assert isinstance(page, EventPage)
    assert type(page.location_blocks.stream_data[0]['value']['location_page']) == int


@pytest.mark.django_db
def test_create_event_page_with_remote_location():
    page = fixtures.remote_location()
    assert isinstance(page, EventPage)
    assert page.title == "Event at remote location"
    assert page.slug == "event-at-remote-location"
    # Add autogenerated streamfield "id" to expected value
    expected_location_blocks = components.remote_location_block()
    expected_location_blocks[0]["id"] = page.location_blocks.stream_data[0]["id"]
    assert page.location_blocks.stream_data == expected_location_blocks


@pytest.mark.django_db
def test_import_event_page_with_remote_location(remote_staging_preview_url, test_api_url, test_api_jwt_token):
    url = f'{remote_staging_preview_url}/event/UGFnZVJldmlzaW9uTm9kZTo0Ng==?CMS_API={test_api_url}'
    page = PageImporter(url, test_api_jwt_token).fetch_page_data().create_page()
    assert isinstance(page, EventPage)
    # Remove autogenerated "id" to see if the rest of stream_data matches
    del page.location_blocks.stream_data[0]["id"]
    assert page.location_blocks.stream_data == [{
        'type': 'remote_location',
        'value': {
            'additional_details_ar': '',
            'additional_details_en': '3rd floor conference room',
            'additional_details_es': '',
            'additional_details_vi': '',
            'city': 'Austin',
            'name_ar': '',
            'name_en': 'Faulk',
            'name_es': '',
            'name_vi': '',
            'state': 'TX',
            'street': '800 Guadalupe',
            'unit': '5',
            'zip': '78701'
        }
    }]


@pytest.mark.django_db
def test_import_event_page_with_fees(remote_staging_preview_url, test_api_url, test_api_jwt_token):
    url = f'{remote_staging_preview_url}/event/UGFnZVJldmlzaW9uTm9kZTo0OA==?CMS_API={test_api_url}'
    page = PageImporter(url, test_api_jwt_token).fetch_page_data().create_page()
    assert isinstance(page, EventPage)
