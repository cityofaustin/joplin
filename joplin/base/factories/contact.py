from base.models.contact import Contact
from factory import DjangoModelFactory


class ContactFactory(DjangoModelFactory):
    class Meta:
        model = Contact
