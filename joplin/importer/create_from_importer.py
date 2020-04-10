import requests
import hashlib

from snippets.contact.models import Contact
from snippets.contact.factories import ContactFactory
from snippets.theme.models import Theme
from pages.topic_collection_page.factories import ThemeFactory
from wagtail.documents.models import Document
from pages.official_documents_page.factories import DocumentFactory
from django.core.files.base import ContentFile
from pages.home_page.models import HomePage
from pages.information_page.models import InformationPage
from pages.information_page.factories import InformationPageFactory
from pages.topic_page.models import TopicPage
from pages.topic_page.factories import TopicPageFactory
from pages.topic_collection_page.models import TopicCollectionPage
from pages.topic_collection_page.factories import TopicCollectionPageFactory
from pages.service_page.models import ServicePage
from pages.service_page.factories import ServicePageFactory
from pages.location_page.models import LocationPage
from pages.location_page.factories import LocationPageFactory
from pages.official_documents_page.models import OfficialDocumentPage
from pages.official_documents_page.factories import OfficialDocumentPageFactory
from pages.department_page.models import DepartmentPage
from pages.department_page.factories import DepartmentPageFactory
from pages.event_page.models import EventPage
from pages.event_page.factories import EventPageFactory

def create_contact_from_importer(contact_data):
    # Check if a contact with the same name has already been imported
    try:
        contact = Contact.objects.get(name=contact_data['name'])
    except Contact.DoesNotExist:
        contact = None
    if contact:
        return contact

    # Check if we have the associated location page
    try:
        location_page_slug = contact_data['location_page']['slug']
        location_page = LocationPage.objects.get(slug=location_page_slug)
    except LocationPage.DoesNotExist:
        location_page = None

    # TODO: handle translation?
    contact_dictionary = {
        'name': contact_data['name'],
        'location_page': location_page
    }

    contact = ContactFactory.create(**contact_dictionary)
    return contact


def create_theme_from_importer(theme_dictionaries):
    # todo: use something other than slug here
    # todo: add imported id to themes
    try:
        theme = Theme.objects.get(slug=theme_dictionaries['en']['slug'])
    except Theme.DoesNotExist:
        theme = None
    if theme:
        return theme

    combined_dictionary = theme_dictionaries['en']
    for field in ThemeFactory._meta.model._meta.fields:
        if field.column.endswith("_es"):
            combined_dictionary[field.column] = theme_dictionaries['es'][field.column[:-3]]

    return ThemeFactory.create(**combined_dictionary)


def create_document_from_importer(document_dictionary):
    # right now we're just going off filename, so first let's see if we can download the file
    # let's try to get it from both the staging and prod s3 buckets (since that's what janis does)
    file_name = document_dictionary['filename']

    for url in [
        f'https://joplin-austin-gov-static.s3.amazonaws.com/production/media/documents/{file_name}',
        f'https://joplin-austin-gov-static.s3.amazonaws.com/staging/media/documents/{file_name}'
    ]:
        response = requests.get(url)
        if response.status_code == 200:
            break

    # wagtail calculates document hashes this way
    # https://github.com/wagtail/wagtail/blob/081705fc7a2d9aec75da25a3593b490f3c145d2b/wagtail/documents/models.py#L115
    file_hash = hashlib.sha1(response.content).hexdigest()

    # Check if a document with the same hash has already been imported
    try:
        document = Document.objects.get(file_hash=file_hash)
    except Document.DoesNotExist:
        document = None
    if document:
        return document

    # It has not been imported, let's do it!
    document = DocumentFactory.create(file=ContentFile(response.content, name=file_name), title=file_name)
    return document


def create_page_from_importer(page_type, page_dictionaries, revision_id=None):
    page_type_map = {
        "information": {
            "model": InformationPage,
            "factory": InformationPageFactory,
        },
        "topics" : {
            "model": TopicPage,
            "factory": TopicPageFactory,
        },
        "topiccollection": {
            "model": TopicCollectionPage,
            "factory": TopicCollectionPageFactory,
        },
        "services": {
            "model": ServicePage,
            "factory": ServicePageFactory,
        },
        "location": {
            "model": LocationPage,
            "factory": LocationPageFactory,
        },
        "official_document": {
            "model": OfficialDocumentPage,
            "factory": OfficialDocumentPageFactory,
        },
        "department": {
            "model": DepartmentPage,
            "factory": DepartmentPageFactory,
        },
        "event": {
            "model": EventPage,
            "factory": EventPageFactory,
        }
    }
    model = page_type_map[page_type]["model"]
    factory = page_type_map[page_type]["factory"]

    # first check to see if we already imported this page
    # if we did, just go to the edit page for it without changing the db
    # todo: maybe change this to allow updating pages in the future?
    try:
        page = model.objects.get(imported_revision_id=revision_id)
    except model.DoesNotExist:
        page = None
    if page:
        return page

    # since we don't have a page matching the revision id, we should look
    # for other matches, for now let's just use english slug
    # todo: figure out what we want the logic around importing a page with the same slug to look like
    try:
        page = model.objects.get(slug=page_dictionaries['en']['slug'])
    except model.DoesNotExist:
        page = None
    if page:
        return page

    # since we don't have a page matching the revision id or the slug
    # make the combined page dictionary
    combined_dictionary = page_dictionaries['en']

    # associate/create topic pages
    # Only would apply for page_types from JanisBasePageWithTopics
    if 'topics' in combined_dictionary:
        topic_pages = []
        for index in range(len(page_dictionaries['en']['topics']['edges'])):
            topic_page_dictionaries = {
                'en': page_dictionaries['en']['topics']['edges'][index]['node']['topic'],
                'es': page_dictionaries['es']['topics']['edges'][index]['node']['topic'],
            }
            revision_id = page_dictionaries['en']['topics']['edges'][index]['node']['topic']['live_revision']['id']
            topic_page = create_page_from_importer(
                'topics',
                topic_page_dictionaries,
                revision_id
            )
            topic_pages.append(topic_page)
        combined_dictionary['add_topics'] = {'topics': topic_pages}

        # remove topics if we have it because:
        # * it's in english only
        # * the factory doesn't know what to do with it
        del combined_dictionary['topics']

    # associate/create topic collection pages
    # Only applies to TopicPages
    if 'topiccollections' in combined_dictionary:
        topic_collection_pages = []
        for index in range(len(page_dictionaries['en']['topiccollections']['edges'])):
            topic_collection_page_dictionaries = {
                'en': page_dictionaries['en']['topiccollections']['edges'][index]['node']['topiccollection'],
                'es': page_dictionaries['es']['topiccollections']['edges'][index]['node']['topiccollection'],
            }
            revision_id = page_dictionaries['en']['topiccollections']['edges'][index]['node']['topiccollection']['live_revision']['id']
            topic_collection_page = create_page_from_importer(
                'topiccollection',
                topic_collection_page_dictionaries,
                revision_id
            )
            topic_collection_pages.append(topic_collection_page)
        combined_dictionary['add_topic_collections'] = {'topic_collections': topic_collection_pages}
        del combined_dictionary['topiccollections']

    # set the theme
    # Only applies to TopicCollectionPages
    # todo: not hardcode langs in here
    if 'theme' in combined_dictionary:
        combined_dictionary['theme'] = create_theme_from_importer({
            'en': page_dictionaries['en']['theme'],
            'es': page_dictionaries['es']['theme']
        })

    # create/associate department directors
    # Only applies to DepartmentPages
    if 'department_directors' in combined_dictionary:
        department_directors = []
        for index in range(len(page_dictionaries['en']['department_directors']['edges'])):
            en_node = page_dictionaries['en']['department_directors']['edges'][index]['node']
            es_node = page_dictionaries['es']['department_directors']['edges'][index]['node']

            combined_node = en_node
            combined_node['title_es'] = es_node['title']
            combined_node['about_es'] = es_node['about']

            department_directors.append(combined_node)
        combined_dictionary['add_department_directors'] = {'department_directors': department_directors}
        del combined_dictionary['department_directors']

    # associate/create contact
    if 'contacts' in combined_dictionary:
        if len(page_dictionaries['en']['contacts']['edges']):
            combined_dictionary['contact'] = create_contact_from_importer(
                page_dictionaries['en']['contacts']['edges'][0]['node']['contact']
            )
        del combined_dictionary['contacts']

    # Handle related_services
    # Only applies to LocationPages
    # todo: maybe get this related service logic working
    # for now, just get the title from the page on related service and clear it out
    if 'related_services' in combined_dictionary:
        combined_dictionary['add_related_services'] = []
        for edge in combined_dictionary['related_services']['edges']:
            location_page_related_service_to_add = edge['node']

            # since we're using a placeholder service, let's at least get the title somewhere to help us find the page
            location_page_related_service_to_add['hours_exceptions'] += location_page_related_service_to_add['related_service']['title']

            # We really are just trying to get hours imported here, but we can't save
            # without having a page FK'd out to, so we use a placeholder service for now.
            # In order to update this, we'll need to go into the location page and manually update the related service
            # Check if page with (english) slug has already been imported
            try:
                related_service = ServicePage.objects.get(slug='placeholder_service_for_hours')
            except ServicePage.DoesNotExist:
                related_service = None
            if not related_service:
                related_service_dictionary = {
                    'parent': HomePage.objects.first(),
                    'title': 'placeholder service for hours',
                    'slug': 'placeholder_service_for_hours'
                }
                related_service = ServicePageFactory.create(**related_service_dictionary)
            del location_page_related_service_to_add['related_service']
            location_page_related_service_to_add['related_service'] = related_service
            combined_dictionary['add_related_services'].append(location_page_related_service_to_add)
        del combined_dictionary['related_services']

    # associate/create documents
    # Only applies to OfficialDocumentPages
    if 'official_documents' in combined_dictionary:
        official_documents_page_documents = []
        for index in range(len(page_dictionaries['en']['official_documents']['edges'])):
            en_node = page_dictionaries['en']['official_documents']['edges'][index]['node']
            es_node = page_dictionaries['es']['official_documents']['edges'][index]['node']
            en_filename = en_node['document']['filename']
            es_filename = es_node['document']['filename']

            combined_node = en_node
            combined_node['title_es'] = es_node['title']
            combined_node['authoring_office_es'] = es_node['authoring_office']
            combined_node['summary_es'] = es_node['summary']
            combined_node['name_es'] = es_node['name']
            combined_node['document'] = create_document_from_importer(en_node['document'])
            # the api gives us the english doc for janis links if we don't have a spanish doc
            # we're assuming we have different filenames for english and spanish docs
            # so we only import the spanish doc if we have a different filename
            if es_filename != en_filename:
                combined_node['document_es'] = create_document_from_importer(es_node['document'])

            official_documents_page_documents.append(combined_node)
        combined_dictionary['add_official_documents_page_documents'] = {'official_documents_page_documents': official_documents_page_documents}
        del combined_dictionary['official_documents']

    # remove liveRevision if we have it
    if 'live_revision' in combined_dictionary:
        del combined_dictionary['live_revision']

    # set the translated fields
    for field in factory._meta.model._meta.fields:
        if field.column.endswith("_es"):
            if field.column[:-3] in page_dictionaries['es']:
                combined_dictionary[field.column] = page_dictionaries['es'][field.column[:-3]]

    # Set home as parent
    '''
        HomePage.objects.first() must be retrieved here at the end of create_page_from_importer(), rather than the beginning.
        Why? Because our HomePage model might have changed during the course of create_page_from_importer() if other pages
        were added (like topics).
        If our 'parent' is an instance of an outdated HomePage, then there will be wagtail path conflicts for your page.
    '''
    combined_dictionary['parent'] = HomePage.objects.first()

    # todo: actually get departments here
    # combined_dictionary['add_department'] = ['just a string']

    page = factory.create(**combined_dictionary)
    return page
