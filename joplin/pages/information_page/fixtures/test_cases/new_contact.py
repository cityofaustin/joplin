import os
from pages.information_page.fixtures.helpers.create_fixture import create_fixture
import pages.information_page.fixtures.helpers.components as components
import snippets.contact.fixtures.helpers.components as contact_components


# An information page with a contact
def new_contact():
    page_data = {
        "imported_revision_id": None,
        "live": False,
        "parent": components.home(),
        "coa_global": False,
        "title": "Information page with new contact",
        "slug": "information-page-with-new-contact",
        "contact": contact_components.new_contact()
    }

    return create_fixture(page_data, os.path.basename(__file__))
