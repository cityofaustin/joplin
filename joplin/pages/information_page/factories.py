import factory
import wagtail_factories
from django.utils.text import slugify
from pages.topic_page.models import TopicPage
from pages.information_page.models import InformationPageContact, InformationPage
from pages.factory import PageFactory
from base.models import Contact
from pytest_factoryboy import register
from wagtail.core.models import Page
from pages.topic_page.factories import JanisBasePageWithTopicsFactory, create_topic_page_from_page_dictionary
from pages.home_page.models import HomePage


class InformationPageFactory(JanisBasePageWithTopicsFactory):
    class Meta:
        model = InformationPage


def create_information_page_from_importer_dictionaries(page_dictionaries, revision_id):
    # leaving this here and moving to topic collection to start
    blargyy = [(field.column, field.column[:-3]) for field in InformationPageFactory._meta.model._meta.fields if
               field.column.endswith("_es")]

    # first check to see if we already imported this page
    # if we did, just go to the edit page for it without changing the db
    # todo: maybe change this to allow updating pages in the future?
    try:
        page = InformationPage.objects.get(imported_revision_id=revision_id)
    except InformationPage.DoesNotExist:
        page = None
    if page:
        return page

    # since we don't have a page matching the revision id, we should look
    # for other matches, for now let's just use english slug
    # todo: figure out what we want the logic around importing a page with the same slug to look like
    try:
        page = InformationPage.objects.get(slug=page_dictionaries['en']['slug'])
    except InformationPage.DoesNotExist:
        page = None
    if page:
        return page

    # since we don't have a page matching the revision id or the slug
    # we need to create a page, which needs a topic if it has one
    # run through the topic logic here
    topic_page_dictionaries = [edge['node']['topic'] for edge in page_dictionary['topics']['edges']]
    topic_pages = [create_topic_page_from_page_dictionary(dictionary, dictionary['liveRevision']['id']) for dictionary
                   in topic_page_dictionaries]

    # todo: actually get departments here
    related_departments = ['just a string']

    # Set home as parent
    # todo: move this to base page factory?
    home = HomePage.objects.first()

    # make the page
    page = InformationPageFactory.create(imported_revision_id=revision_id, title=page_dictionary['title'],
                                         slug=page_dictionary['slug'], description=page_dictionary['description'],
                                         add_topics={'topics': topic_pages}, add_related_departments=related_departments,
                                         additional_content=page_dictionary['additionalContent'],
                                         coa_global=page_dictionary['coaGlobal'], parent=home)

    return page
