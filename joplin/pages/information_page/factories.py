import factory
import wagtail_factories
from django.utils.text import slugify
from pages.topic_page.models import TopicPage
from pages.information_page.models import InformationPageContact, InformationPage
from pages.factory import PageFactory
from base.models import Contact
from pytest_factoryboy import register
from wagtail.core.models import Page
from pages.topic_page.factories import JanisBasePageWithTopicsFactory, create_topic_page_from_importer_dictionaries
from pages.home_page.models import HomePage


class InformationPageFactory(JanisBasePageWithTopicsFactory):
    class Meta:
        model = InformationPage


def create_information_page_from_importer_dictionaries(page_dictionaries, revision_id):
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
    # make the combined page dictionary
    combined_dictionary = page_dictionaries['en']

    # associate/create topic pages
    topic_pages = []
    for index in range(len(page_dictionaries['en']['topics']['edges'])):
        topic_pages.append(create_topic_page_from_importer_dictionaries({
            'en': page_dictionaries['en']['topics']['edges'][index]['node']['topic'],
            'es': page_dictionaries['es']['topics']['edges'][index]['node']['topic'],
        }, page_dictionaries['en']['topics']['edges'][index]['node']['topic']['live_revision']['id']))
    combined_dictionary['add_topics'] = {'topics': topic_pages}

    # remove topics if we have it because:
    # * it's in english only
    # * the factory doesn't know what to do with it
    # todo: why isn't pop working?
    if 'topics' in combined_dictionary:
        del combined_dictionary['topics']

    # remove contacts if we have it because:
    # * it might be what's wrong rn
    # todo: why isn't pop working?
    if 'contacts' in combined_dictionary:
        del combined_dictionary['contacts']


    # Set home as parent
    combined_dictionary['parent'] = HomePage.objects.first()

    # set the translated fields
    for field in InformationPageFactory._meta.model._meta.fields:
        if field.column.endswith("_es"):
            if field.column[:-3] in page_dictionaries['es']:
                combined_dictionary[field.column] = page_dictionaries['es'][field.column[:-3]]

    # todo: actually get departments here
    # combined_dictionary['add_related_departments'] = ['just a string']

    page = InformationPageFactory.create(**combined_dictionary)
    return page
