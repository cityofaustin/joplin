from snippets.contact.models import Contact
from factory import DjangoModelFactory


class ContactFactory(DjangoModelFactory):
    class Meta:
        model = Contact


# def create_contact_from_importer_dictionaries(page_dictionaries, revision_id=None):
