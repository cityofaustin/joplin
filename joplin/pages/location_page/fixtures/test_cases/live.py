import os
from pages.location_page.fixtures.helpers.create_fixture import create_fixture
import pages.location_page.fixtures.helpers.components as components


def live():
    page_data = {
        "imported_revision_id": None,
        "live": True,
        "parent": components.home(),
        "coa_global": False,
        "title": "Live Location page",
        "slug": "live-location-page",
    }

    return create_fixture(page_data, os.path.basename(__file__))
