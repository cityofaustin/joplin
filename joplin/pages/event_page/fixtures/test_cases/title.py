import os
from pages.event_page.fixtures.helpers.create_fixture import create_fixture
import pages.event_page.fixtures.helpers.components as components


# A event page with only a title
def title():
    page_data = {
        "imported_revision_id": None,
        "live": False,
        "parent": components.home(),
        "coa_global": False,
        "title": "Event page with title",
        "slug": "Event-page-with-title",
    }

    return create_fixture(page_data, os.path.basename(__file__))
