import pytest
from pages.information_page.models import InformationPage
from pages.topic_page.factories import TopicPageFactory
from pages.information_page.factories import InformationPageFactory
from humps import decamelize
from importer.page_importer import PageImporter
import pages.information_page.fixtures as fixtures

from importer.create_from_importer import create_page_from_importer
create_topic_page_from_importer_dictionaries = lambda page_dictionaries, revision_id=None: create_page_from_importer('topics', page_dictionaries, revision_id)
create_information_page_from_importer_dictionaries = lambda page_dictionaries, revision_id=None: create_page_from_importer('information', page_dictionaries, revision_id)

def page_dictionaries():
    return decamelize({
        'en': {
            'title': 'information page title [en]',
            'slug': 'information-page-title-en',
            'description': 'information page description [en]',
            'contacts': {'edges': []},
            'topics': {
                'edges': [{
                    'node': {
                        'topic': {
                            'title': 'topic title [en]',
                            'slug': 'topic-title-en',
                            'description': 'topic description [en]',
                            'topiccollections': {
                                'edges': [{
                                    'node': {
                                        'topiccollection': {
                                            'title': 'topic collection title [en]',
                                            'slug': 'topic-collection-title-en',
                                            'description': 'topic collection description [en]',
                                            'theme': {
                                                'slug': 'theme-slug-en',
                                                'text': 'theme text [en]',
                                                'description': 'theme description [en]'
                                            },
                                            'liveRevision': {
                                                'id': 'UGFnZVJldmlzaW9uTm9kZToz'
                                            }
                                        }
                                    }
                                }]
                            },
                            'liveRevision': {
                                'id': 'UGFnZVJldmlzaW9uTm9kZToxMg=='
                            }
                        }
                    }
                }]
            },
            'additionalContent': '<p>information page additional content [en]</p>',
            'coaGlobal': False
        },
        'es': {
            'title': 'information page title [es]',
            'slug': 'information-page-title-es',
            'description': 'information page description [es]',
            'topics': {
                'edges': [{
                    'node': {
                        'topic': {
                            'title': 'topic title [es]',
                            'slug': 'topic-title-es',
                            'description': 'topic description [es]',
                            'topiccollections': {
                                'edges': [{
                                    'node': {
                                        'topiccollection': {
                                            'title': 'topic collection title [es]',
                                            'slug': 'topic-collection-title-es',
                                            'description': 'topic collection description [es]',
                                            'theme': {
                                                'slug': 'theme-slug-es',
                                                'text': 'theme text [es]',
                                                'description': 'theme description [es]'
                                            },
                                            'liveRevision': {
                                                'id': 'UGFnZVJldmlzaW9uTm9kZToz'
                                            }
                                        }
                                    }
                                }]
                            },
                            'liveRevision': {
                                'id': 'UGFnZVJldmlzaW9uTm9kZToxMg=='
                            }
                        }
                    }
                }]
            },
            'additionalContent': '<p>information page additional content [es]</p>',
            'coaGlobal': False
        }
    })


# when importing the same page twice, we should just
# return the id of the previously imported page
@pytest.mark.django_db
def test_import_from_page_dictionary_twice():
    revision_id = 'UGFnZVJldmlzaW9uTm9kZToxMQ=='

    # get the page we're creating
    page = create_information_page_from_importer_dictionaries(page_dictionaries(), revision_id)

    # try making it again
    second_page = create_information_page_from_importer_dictionaries(page_dictionaries(), revision_id)

    assert second_page == page
    # not sure if we need to check this or not so I'm checking it
    assert list(page.topics.all()) == list(second_page.topics.all())


# when importing the same page twice, with a different revision id
# we should just return the id of the previously imported page
# todo: decide if this is how we want this to work
@pytest.mark.django_db
def test_import_from_page_dictionary_twice_different_revisions():
    first_revision_id = 'first_revision_id'
    second_revision_id = 'second_revision_id'

    # get the page we're creating
    page = create_information_page_from_importer_dictionaries(page_dictionaries(), first_revision_id)

    # try making it again
    second_page = create_information_page_from_importer_dictionaries(page_dictionaries(), second_revision_id)

    assert second_page == page
    # not sure if we need to check this or not so I'm checking it
    assert list(page.topics.all()) == list(second_page.topics.all())


# when importing a page with an existing topic,
# we should use the existing topic for the page
@pytest.mark.django_db
def test_import_from_page_dictionary_existing_topic():
    revision_id = 'UGFnZVJldmlzaW9uTm9kZToxMQ=='
    topic_page_revision_id = page_dictionaries()['en']['topics']['edges'][0]['node']['topic']['live_revision']['id']

    topic_page_dictionaries = {
        'en': page_dictionaries()['en']['topics']['edges'][0]['node']['topic'],
        'es': page_dictionaries()['es']['topics']['edges'][0]['node']['topic']
    }
    topic_pages = [create_topic_page_from_importer_dictionaries(topic_page_dictionaries, topic_page_revision_id)]

    page = create_information_page_from_importer_dictionaries(page_dictionaries(), revision_id)

    topics_on_page = [base_page_topic.topic for base_page_topic in page.topics.all()]

    assert topics_on_page == topic_pages


@pytest.mark.django_db
def test_create_information_page_with_contact_from_api(remote_staging_preview_url, test_api_url, test_api_jwt_token):
    url = f'{remote_staging_preview_url}/information/UGFnZVJldmlzaW9uTm9kZToyMg==?CMS_API={test_api_url}'
    page = PageImporter(url, test_api_jwt_token).fetch_page_data().create_page()
    assert isinstance(page, InformationPage)
    assert page.title == 'Information page with contact'
    assert page.contact.name == 'Contact name'


@pytest.mark.django_db
def test_create_information_page_with_new_contact():
    page = fixtures.new_contact()
    assert isinstance(page, InformationPage)

    assert page.title == 'Information page with new contact'
    assert page.contact.name == 'New contact'
