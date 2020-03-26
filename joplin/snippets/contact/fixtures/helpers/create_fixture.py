from snippets.contact.models import Contact
from snippets.contact.factories import ContactFactory


# Skips creating fixture if Contact with name already exists
def create_fixture(contact_data, fixture_name):
    try:
        contact = Contact.objects.get(name=contact_data['name'])
    except Contact.DoesNotExist:
        contact = None
    if contact:
        print(f"Skipping {fixture_name}")
        return None

    contact = ContactFactory.create(**contact_data)
    print(f"Built {fixture_name}")
    return contact
