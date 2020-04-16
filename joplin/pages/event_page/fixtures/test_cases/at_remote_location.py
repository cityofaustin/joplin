import os
from pages.event_page.fixtures.helpers.create_fixture import create_fixture
import pages.event_page.fixtures.helpers.components as components


# An event page at a city_location
def at_remote_location():
    page_data = {
        "imported_revision_id": None,
        "live": False,
        "parent": components.home(),
        "coa_global": False,
        "title": "Event at remote location",
        "slug": "event-at-remote-location",
        "registration_url": "http://google.com",
        "event_is_free": True,
        "description": "This event is at a remote location.",
        "date": '2020-03-10',
        "start_time": '14:00:00',
        "end_time": '15:00:00',
        "location_blocks": components.remote_location_block(),
    }

    return create_fixture(page_data, os.path.basename(__file__))
