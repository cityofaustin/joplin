import os
from pages.event_page.fixtures.helpers.create_fixture import create_fixture
import pages.event_page.fixtures.helpers.components as components


# A event page that has 3 fee options
def three_fees():
    page_data = {
        "imported_revision_id": None,
        "live": False,
        "parent": components.home(),
        "coa_global": False,
        "title": "Event with fees",
        "slug": "event-with-fees",
        "registration_url": "http://google.com",
        "event_is_free": False,
        "add_fees": {
            "fees": components.three_fees,
        },
        "description": "This event costs money.",
        "date": '2020-03-10',
        "start_time": '14:00:00',
        "end_time": '15:00:00',
        "location_blocks": components.remote_location_block(),
    }

    return create_fixture(page_data, os.path.basename(__file__))
