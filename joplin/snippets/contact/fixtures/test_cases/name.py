import os
from pages.service_page.fixtures.helpers.create_fixture import create_fixture
import pages.service_page.fixtures.helpers.components as components


# A contact with only a name
def name():
    contact_data = {
        "name": "Contact name",
    }

    return create_fixture(contact_data, os.path.basename(__file__))
