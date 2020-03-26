import factory
import json
import wagtail_factories
from django.utils.text import slugify
from pages.topic_page.models import TopicPage
from pages.service_page.models import ServicePage
from pages.factory import PageFactory
from base.models import Contact
from pytest_factoryboy import register
from wagtail.core.models import Page
from pages.topic_page.factories import JanisBasePageWithTopicsFactory, create_topic_page_from_importer_dictionaries
from pages.home_page.models import HomePage

from base.models.contact import Contact
from factory import DjangoModelFactory


class ContactFactory(DjangoModelFactory):
    class Meta:
        model = Contact


# def create_contact_from_importer_dictionaries(page_dictionaries, revision_id=None):
