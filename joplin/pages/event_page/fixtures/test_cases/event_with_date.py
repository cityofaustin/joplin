import os
from pages.event_page.fixtures.helpers.create_fixture import create_fixture
import pages.event_page.fixtures.helpers.components as components


# A event page with only a title
def event_with_date():
    page_data = {
        "imported_revision_id": None,
        "live": True,
        "parent": components.home(),
        "coa_global": False,
        "title": "Event page with date",
        "slug": "Event-page-with-date",
        "date": "1984-9-5",
    }

    return create_fixture(page_data, os.path.basename(__file__))
