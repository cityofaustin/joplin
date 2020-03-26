import pytest

from snippets.contact.models import Contact
import snippets.contact.fixtures as fixtures


@pytest.mark.django_db
def test_create_contact_with_name():
    contact = fixtures.name()
    assert isinstance(contact, Contact)
    assert contact.name == "Service Page with title"

