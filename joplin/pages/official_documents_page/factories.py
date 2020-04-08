import factory
import wagtail_factories
from django.utils.text import slugify
from wagtail.core.models import Collection, Page
from pages.official_documents_page.models import OfficialDocumentPage
from pages.factory import PageFactory
from pages.topic_page.factories import TopicPageFactory

from pages.topic_page.factories import JanisBasePageWithTopicsFactory, create_topic_page_from_importer_dictionaries
from pages.home_page.models import HomePage

class OfficialDocumentPageFactory(JanisBasePageWithTopicsFactory):
    class Meta:
        model = OfficialDocumentPage



def create_official_documents_page_from_importer_dictionaries(page_dictionaries, revision_id=None):
    # Check if page with revision_id has already been imported
    if revision_id:
        try:
            page = OfficialDocumentPage.objects.get(imported_revision_id=revision_id)
        except OfficialDocumentPage.DoesNotExist:
            page = None
        if page:
            return page

    # Check if page with (english) slug has already been imported
    try:
        page = OfficialDocumentPage.objects.get(slug=page_dictionaries['en']['slug'])
    except OfficialDocumentPage.DoesNotExist:
        page = None
    if page:
        return page

    # since we don't have a page matching the revision id or the slug
    # make the combined page dictionary
    combined_dictionary = page_dictionaries['en']

    # todo: figure out where to move this so it isn't copypasta in information page
    # associate/create topic pages
    topic_pages = []
    for index in range(len(page_dictionaries['en']['topics']['edges'])):
        topic_pages.append(create_topic_page_from_importer_dictionaries({
            'en': page_dictionaries['en']['topics']['edges'][index]['node']['topic'],
            'es': page_dictionaries['es']['topics']['edges'][index]['node']['topic'],
        }, page_dictionaries['en']['topics']['edges'][index]['node']['topic']['live_revision']['id']))
    combined_dictionary['add_topics'] = {'topics': topic_pages}

    # remove topics if we have it because:
    # * we just added it up above
    # todo: why isn't pop working?
    if 'topics' in combined_dictionary:
        del combined_dictionary['topics']

    # Set home as parent
    combined_dictionary['parent'] = HomePage.objects.first()

    # set the translated fields
    for field in OfficialDocumentPageFactory._meta.model._meta.fields:
        if field.column.endswith("_es"):
            if field.column[:-3] in page_dictionaries['es']:
                combined_dictionary[field.column] = page_dictionaries['es'][field.column[:-3]]


    # todo: actually get departments here
    # combined_dictionary['add_department'] = ['just a string']

    # todo: get the actual docs

    page = OfficialDocumentPageFactory.create(**combined_dictionary)
    return page
