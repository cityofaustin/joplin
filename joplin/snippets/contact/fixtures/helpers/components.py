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


def mvp_news_contact():
    contact_data = {
        "name": "MVP news contact",
        "email": "Email.Address@austintexas.gov",
        "add_phone_numbers": [{"phone_description": "Office", "phone_number": "+15129742220"}]

    }

    return create_fixture(contact_data, os.path.basename(__file__))


def mvp_news_contact_extended():
    contact_data = {
        "name": "MVP news contact (extended)",
        "email": "Email.Address@austintexas.gov",
        "add_phone_numbers": [{"phone_description": "Office", "phone_number": "+15129742220"},
                              {"phone_description": "24/7 help line", "phone_number": "+18008675309"}],
        "social_media": [
            {
                "type": "url",
                "value": "http://facebook.com/fake/"
            },
            {
                "type": "url",
                "value": "http://twitter.com/fake/"
            }
        ]

    }

    return create_fixture(contact_data, os.path.basename(__file__))
