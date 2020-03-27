import os
from pages.location_page.fixtures.helpers.create_fixture import create_fixture
import pages.location_page.fixtures.helpers.components as components


# A Service page with only a title
def title():
    page_data = {
        "imported_revision_id": None,
        "live": False,
        "parent": components.home(),
        "coa_global": False,
        "title": "Location page with title",
        "slug": "location-page-with-title",
    }

    return create_fixture(page_data, os.path.basename(__file__))
