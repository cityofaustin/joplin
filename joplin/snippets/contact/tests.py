import pytest

from snippets.contact.models import Contact
import snippets.contact.fixtures as fixtures
from importer.create_from_importer import create_contact_from_importer


@pytest.mark.django_db
def test_create_contact_with_name():
    contact = fixtures.name()
    assert isinstance(contact, Contact)
    assert contact.name == "Contact name"


@pytest.mark.django_db
def test_import_contact_with_no_location_page():
    contact_data = {
        "name": "A contact without a LocationPage",
        "location_page": None,
    }
    contact = create_contact_from_importer(contact_data)
    assert isinstance(contact, Contact)
    assert contact.name == "A contact without a LocationPage"
