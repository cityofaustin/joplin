import factory
import wagtail_factories
from django.utils.text import slugify
from wagtail.core.models import Collection, Page
from pages.official_documents_page.models import OfficialDocumentPage, OfficialDocumentPageDocument
from pages.factory import PageFactory
from pages.topic_page.factories import TopicPageFactory

from pages.topic_page.factories import JanisBasePageWithTopicsFactory, create_topic_page_from_importer_dictionaries
from pages.home_page.models import HomePage
from wagtail.documents.models import Document


class OfficialDocumentPageFactory(JanisBasePageWithTopicsFactory):
    class Meta:
        model = OfficialDocumentPage

    @factory.post_generation
    def add_official_documents_page_documents(self, create, extracted, **kwargs):
        # TODO: add option to pass in already created topics
        if extracted:
            # A list of topics were passed in, use them
            for add_official_documents_page_document in extracted['official_documents_page_documents']:
                official_docs_blarg = extracted['official_documents_page_documents']
                OfficialDocumentPageDocumentFactory.create(page=self, **official_docs_blarg)
            return


class DocumentFactory(factory.DjangoModelFactory):
    @classmethod
    def create(cls, *args, **kwargs):
        # todo: document file stuff here
        return super(DocumentFactory, cls).create(*args, **kwargs)

    class Meta:
        model = Document


class OfficialDocumentPageDocumentFactory(factory.DjangoModelFactory):
    page = factory.SubFactory(
        'official_documents_page.factories.OfficialDocumentsPageFactory',
    )

    document = factory.SubFactory(
        DocumentFactory
    )

    class Meta:
        model = OfficialDocumentPageDocument


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

    # associate/create documents
    official_documents_page_documents = []
    for index in range(len(page_dictionaries['en']['official_documents']['edges'])):
        en_node = page_dictionaries['en']['official_documents']['edges'][index]['node']
        es_node = page_dictionaries['es']['official_documents']['edges'][index]['node']

        en_node['document'] = create_document_from_importer_dictionary(en_node['document'])
        es_node['document'] = create_document_from_importer_dictionary(es_node['document'])

        official_documents_page_documents.append({
            'en': en_node,
            'es': es_node,
        })
    combined_dictionary['add_official_documents_page_documents'] = {'official_documents_page_documents': official_documents_page_documents}

    # remove topics if we have it because:
    # * we just added it up above
    # todo: why isn't pop working?
    if 'topics' in combined_dictionary:
        del combined_dictionary['topics']


    page = OfficialDocumentPageFactory.create(**combined_dictionary)
    return page


def create_document_from_importer_dictionary(document_dictionary):
    for field in DocumentFactory._meta.model._meta.fields:
        blarg = 3

    # Check if a document with the same filename has already been imported
    try:
        document = Document.objects.get(filename=document_dictionary['filename'])
    except Document.DoesNotExist:
        document = None
    if document:
        return document

    document_dictionary = {
        'name': 'blarg',
    }

    return None

    document = DocumentFactory.create(**document_dictionary)
    return document
