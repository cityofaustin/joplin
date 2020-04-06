import factory
from snippets.contact.models import Contact
from pages.location_page.models import LocationPage
from factory import DjangoModelFactory


class ContactFactory(DjangoModelFactory):

    class Meta:
        model = Contact


def create_contact_from_importer_dictionaries(page_dictionaries):
    # Check if a contact with the same name has already been imported
    try:
        contact = Contact.objects.get(name=page_dictionaries['en']['contacts']['edges'][0]['node']['contact']['name'])
    except Contact.DoesNotExist:
        contact = None
    if contact:
        return contact

    contact_dictionary = {
        'name': page_dictionaries['en']['contacts']['edges'][0]['node']['contact']['name'],
        'location_page': LocationPage.objects.first()
    }

    contact = ContactFactory.create(**contact_dictionary)
    return contact
