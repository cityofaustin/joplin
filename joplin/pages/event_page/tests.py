import pytest

from pages.event_page.models import EventPage
import pages.event_page.fixtures as fixtures
from pages.event_page.factories import EventPageFactory


@pytest.mark.django_db
def test_create_event_page_with_title():
    page = fixtures.title()
    assert isinstance(page, EventPage)
    assert page.title == "Event page with title"
    assert page.slug == "Event-page-with-title"


# If Event page has janis url
# and coa_global=False (top level is not checked)
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
