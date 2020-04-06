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
