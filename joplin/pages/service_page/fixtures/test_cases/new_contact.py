import os
from pages.service_page.fixtures.helpers.create_fixture import create_fixture
import pages.service_page.fixtures.helpers.components as components


# A Service page with only a title
def new_contact():
    page_data = {
        "imported_revision_id": None,
        "live": False,
        "parent": components.home(),
        "coa_global": False,
        "title": "Service page with new contact",
        "slug": "service-page-with-new-contact",
        "contact": components.new_contact()
    }

    return create_fixture(page_data, os.path.basename(__file__))
