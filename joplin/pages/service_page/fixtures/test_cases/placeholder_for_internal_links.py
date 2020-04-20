import os
from pages.service_page.fixtures.helpers.create_fixture import create_fixture
import pages.service_page.fixtures.helpers.components as components


# A placeholder service page for internal links
def placeholder_for_internal_links():
    page_data = {
        "imported_revision_id": None,
        "live": False,
        "parent": components.home(),
        "coa_global": False,
        "title": "Placeholder service page for internal links",
        "slug": "placeholder_service_page_for_internal_links",
    }

    return create_fixture(page_data, os.path.basename(__file__))
