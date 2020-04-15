import os
from pages.event_page.fixtures.helpers.create_fixture import create_fixture
import pages.event_page.fixtures.helpers.components as components


# A event page with a city_location
def city_location():
    location_blocks = components.city_location_block()
    # home() must be invoked after a foreign location_page is created in components.city_location_block()
    home = components.home()
    page_data = {
        "imported_revision_id": None,
        "live": False,
        "parent": home,
        "coa_global": False,
        "title": "Event page at City Location",
        "slug": "event-page-at-city-location",
        "registration_url": "http://fake.url",
        "event_is_free": True,
        "description": "This event is at a City Location.",
        "date": '2020-03-10',
        "start_time": '14:00:00',
        "end_time": '15:00:00',
        "location_blocks": location_blocks,
    }

    return create_fixture(page_data, os.path.basename(__file__))
