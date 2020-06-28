import requests
import hashlib
from django.core.exceptions import ValidationError
from distutils.util import strtobool

from pages.base_page.fixtures.helpers.page_type_map import page_type_map
from snippets.contact.models import Contact
from snippets.contact.factories import ContactFactory
from snippets.theme.models import Theme
from pages.topic_collection_page.factories import ThemeFactory
from wagtail.documents.models import Document
# from pages.official_documents_page.factories import DocumentFactory
from django.core.files.base import ContentFile
from users.models import User
from users.factories import UserFactory
from pages.home_page.models import HomePage
from pages.location_page.models import LocationPage
from pages.service_page.models import ServicePage
from pages.service_page.factories import ServicePageFactory
from groups.models import Department
from groups.factories import DepartmentFactory


def create_contact_from_importer(contact_data):
    # Check if a contact with the same name has already been imported
    try:
        contact = Contact.objects.get(name=contact_data['name'])
    except Contact.DoesNotExist:
        contact = None
    if contact:
        return contact

    # Check if we have the associated location page
    if contact_data['location_page']:
        try:
            location_page_slug = contact_data['location_page']['slug']
            location_page = LocationPage.objects.get(slug=location_page_slug)
        except LocationPage.DoesNotExist:
            location_page = None
    else:
        location_page = None

    contact_dictionary = {
        'name': contact_data['name'],
        'location_page': location_page
    }

    contact = ContactFactory.create(**contact_dictionary)
    return contact


def create_theme_from_importer(theme_dictionaries):
    # todo: use something other than slug here
    # todo: add imported id to themes

    # if we don't have a theme, don't try
    if theme_dictionaries['en'] is None:
        return None

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
    file_size = document_dictionary['file_size']

    for url in [
        f'https://joplin3-austin-gov-static.s3.amazonaws.com/production/media/documents/{file_name}',
        f'https://joplin3-austin-gov-static.s3.amazonaws.com/staging/media/documents/{file_name}',
        f'https://joplin-austin-gov-static.s3.amazonaws.com/production/media/documents/{file_name}',
        f'https://joplin-austin-gov-static.s3.amazonaws.com/staging/media/documents/{file_name}',
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
    document = DocumentFactory.create(file=ContentFile(response.content, name=file_name), title=file_name, file_size=file_size)
    return document


def create_owner_from_importer(owner_data):
    # Check if we have any owner data
    # example: the ARR department page doesn't have any
    if not owner_data:
        return

    # Check if a user with the same name has already been imported
    try:
        user = User.objects.get(email=owner_data['email'])
    except User.DoesNotExist:
        user = None
    if user:
        return user

    # TODO: add ability to import non-superusers (and handle their departments and specific permissions)
    owner_data["is_superuser"] = bool(strtobool(owner_data["is_superuser"]))
    if not owner_data["is_superuser"]:
        raise ValidationError("Only allowing imports for pages owned by superusers.")

    user = UserFactory.create(**owner_data)
    return user


def create_department_group_from_importer(department_page_dictionaries):
    # see if we already have a department group associated with this department page information
    try:
        department_group = Department.objects.get(department_page__slug=department_page_dictionaries['en']['slug'])
    except Department.DoesNotExist:
        department_group = None
    if department_group:
        return department_group

    # we don't have the department group for this page
    # create or get the department page
    # todo: figure out how to get a revision id for departments that aren't live
    department_page_revision_id = None
    if department_page_dictionaries['en']['live_revision']:
        department_page_revision_id = department_page_dictionaries['en']['live_revision']['id']
    department_page = create_page_from_importer('department', department_page_dictionaries, department_page_revision_id)

    # and make the group
    department_group = DepartmentFactory.create(department_page=department_page, name=department_page.title)
    return department_group


def create_page_from_importer(page_type, page_dictionaries, revision_id=None):
    model = page_type_map[page_type]["model"]
    factory = page_type_map[page_type]["factory"]

    # If we have a revision id, try getting the page using it
    # if we don't check this, we'll get matches on revision_id=None
    if revision_id:
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

    combined_dictionary['imported_revision_id'] = revision_id

    # associate/create topic pages
    # Only would apply for page_types from JanisBasePageWithTopics
    if 'topics' in combined_dictionary:
        topic_pages = []
        for index in range(len(page_dictionaries['en']['topics']['edges'])):
            topic_page_dictionaries = {
                'en': page_dictionaries['en']['topics']['edges'][index]['node']['topic'],
                'es': page_dictionaries['es']['topics']['edges'][index]['node']['topic'],
            }

            live_revision = page_dictionaries['en']['topics']['edges'][index]['node']['topic']['live_revision']
            if live_revision:
                revision_id = live_revision['id']

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

    # remove physical location photo from location pages until we support importing images
    if 'physical_location_photo' in combined_dictionary:
        del combined_dictionary['physical_location_photo']

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

    # associate/create departments
    if 'departments' in combined_dictionary:
        department_groups = []
        for index in range(len(page_dictionaries['en']['departments'])):
            department_group_dictionaries = {
                'en': page_dictionaries['en']['departments'][index],
                'es': page_dictionaries['es']['departments'][index],
            }
            department_group = create_department_group_from_importer(department_group_dictionaries)
            department_groups.append(department_group)
        combined_dictionary['add_departments'] = {'departments': department_groups}

        # remove departments if we have it because:
        # * it's in english only
        # * the factory doesn't know what to do with it
        del combined_dictionary['departments']

    # Only applies to 'event' page_type
    if page_type is 'event':
        # Associate locations to event pages
        if 'locations' in combined_dictionary:
            location_blocks = []
            for index, location in enumerate(page_dictionaries['en']['locations']):
                is_city_location = location['location_type'] == 'city_location'
                if is_city_location:
                    location_page_dictionaries = {
                        'en': page_dictionaries['en']['locations'][index]["city_location"],
                        'es': page_dictionaries['es']['locations'][index]["city_location"],
                    }
                    revision_id = location["city_location"]['live_revision']['id']
                    location_page = create_page_from_importer(
                        'location',
                        location_page_dictionaries,
                        revision_id,
                    )
                    # Steamfield only wants the Primary Key of the city_location.
                    # Overwrite with the pk of your newly created/retrieved location_page.
                    location["value"]["location_page"] = location_page.pk
                    location_block = {
                        "type": "city_location",
                        "value": location["value"],
                    }
                else:
                    location_block = {
                        "type": "remote_location",
                        "value": location["value"],
                    }
                location_blocks.append(location_block)
            combined_dictionary['location_blocks'] = location_blocks
            del combined_dictionary['locations']
        if 'fees' in combined_dictionary:
            fees = []
            for index, fee in enumerate(page_dictionaries['en']['fees']['edges']):
                en_node = page_dictionaries['en']['fees']['edges'][index]['node']
                es_node = page_dictionaries['es']['fees']['edges'][index]['node']
                combined_node = en_node
                combined_node['fee_label_es'] = es_node["fee_label"]
                fees.append(combined_node)
            combined_dictionary['add_fees'] = {'fees': fees}
            del combined_dictionary['fees']

    # set the translated fields
    # by doing this before the steps logic, we can make sure to not import english steps into spanish step fields
    for field in factory._meta.model._meta.fields:
        if field.column.endswith("_es"):
            if field.column[:-3] in page_dictionaries['es']:
                # make sure we aren't just getting the english fallback value
                # https://wagtail-modeltranslation-docs.readthedocs.io/en/latest/Advanced%20Settings.html#fallback-languages
                if page_dictionaries['es'][field.column[:-3]] != page_dictionaries['en'][field.column[:-3]]:
                    combined_dictionary[field.column] = page_dictionaries['es'][field.column[:-3]]

    # Handle 'steps_with_locations' in services
    if page_type is 'services':
        for lang in ['', '_es']:
            if f'steps{lang}' in combined_dictionary:
                '''
                Important note!
                We are iterating through copies of each list.
                Note the slice [:] on combined_dictionary["steps"][:].
                We need to iterate through copies of these lists, because some pieces of logic
                will require us to delete the indexes that we're iterating on.
                Make sure that you're modifying/deleting the original list, not the copy[:] that
                you're iterating through.
                '''
                for i, step in enumerate(combined_dictionary[f'steps{lang}'][:]):
                    # Only import step with location if we have that location already.
                    if step['type'] == 'step_with_locations':
                        removed_locations = False
                        for j, location in enumerate(step["value"]["locations"][:]):
                            # Add location_page data only if location was already imported.
                            # Right now, a "step_with_location" does not provide enough location_page
                            # data required to import a new location_page.
                            try:
                                location_page = LocationPage.objects.get(slug=location["location_page"]['slug'])
                            except LocationPage.DoesNotExist:
                                location_page = None
                            if location_page:
                                combined_dictionary[f'steps{lang}'][i]["value"]["locations"][j] = location_page.pk
                            else:
                                removed_locations = True
                                del combined_dictionary[f'steps{lang}'][i]["value"]["locations"][j]
                        if removed_locations:
                            # If all locations were removed from step, then delete the step
                            if not len(step["value"]["locations"]):
                                del combined_dictionary[f'steps{lang}'][i]
                            # If any locations were removed, then make sure the Service_Page is not published
                            combined_dictionary["live"] = False

    # remove liveRevision if we have it
    if 'live_revision' in combined_dictionary:
        del combined_dictionary['live_revision']

    # set the owner of the page
    if 'owner' in combined_dictionary:
        combined_dictionary['owner'] = create_owner_from_importer(combined_dictionary['owner'])

    # Set home as parent
    '''
        HomePage.objects.first() must be retrieved here at the end of create_page_from_importer(), rather than the beginning.
        Why? Because our HomePage model might have changed during the course of create_page_from_importer() if other pages
        were added (like topics).
        If our 'parent' is an instance of an outdated HomePage, then there will be wagtail path conflicts for your page.
    '''
    combined_dictionary['parent'] = HomePage.objects.first()

    page = factory.create(**combined_dictionary)
    return page
