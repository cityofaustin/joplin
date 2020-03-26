import os
from snippets.contact.fixtures.helpers.create_fixture import create_fixture


# A contact with only a name
def name():
    contact_data = {
        "name": "Contact name",
    }

    return create_fixture(contact_data, os.path.basename(__file__))
