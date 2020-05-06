'''
    components.py contains elements that may be used
    interchangeably with multiple fixtures
'''
import os
from snippets.contact.fixtures.helpers.create_fixture import create_fixture


def new_contact():
    contact_data = {
        "name": "New contact",
    }

    return create_fixture(contact_data, os.path.basename(__file__))


def mvp_media_release_contact():
    contact_data = {
        "name": "",
        "add_phone_numbers": [{"phone_description": "Office", "phone_number": "+15129742220"}]
    }

    return create_fixture(contact_data, os.path.basename(__file__))
