import factory
from snippets.contact.models import Contact, ContactPhoneNumber
from pages.location_page.models import LocationPage
from factory import DjangoModelFactory


class ContactPhoneNumberFactory(DjangoModelFactory):

    class Meta:
        model = ContactPhoneNumber


class ContactFactory(DjangoModelFactory):

    class Meta:
        model = Contact

    @factory.post_generation
    def add_phone_numbers(self, create, extracted, **kwargs):
        if extracted:
            # A list of phone numbers were passed in, use them
            for phone_number in extracted:
                ContactPhoneNumberFactory.create(contact=self, phone_description=phone_number['phone_description'], phone_number=phone_number['phone_number'])
            return


def create_contact_from_importer_dictionaries(page_dictionaries):
    # Check if a contact with the same name has already been imported
    try:
        contact = Contact.objects.get(name=page_dictionaries['en']['contacts']['edges'][0]['node']['contact']['name'])
    except Contact.DoesNotExist:
        contact = None
    if contact:
        return contact

    # Check if we have the associated location page
    try:
        location_page_slug = page_dictionaries['en']['contacts']['edges'][0]['node']['contact']['location_page']['slug']
        location_page = LocationPage.objects.get(slug=location_page_slug)
    except LocationPage.DoesNotExist:
        location_page = None

    contact_dictionary = {
        'name': page_dictionaries['en']['contacts']['edges'][0]['node']['contact']['name'],
        'location_page': location_page
    }

    contact = ContactFactory.create(**contact_dictionary)
    return contact
