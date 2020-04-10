import pytest
from humps import decamelize

# Try importing using dummy data in a page_dictionary
from pages.topic_collection_page.factories import ThemeFactory, TopicCollectionPageFactory
from pages.topic_page.factories import TopicPageFactory

from importer.create_from_importer import create_page_from_importer
create_topic_page_from_importer_dictionaries = lambda page_dictionaries, revision_id=None: create_page_from_importer('topics', page_dictionaries, revision_id)
create_topic_collection_page_from_importer_dictionaries = lambda page_dictionaries, revision_id=None: create_page_from_importer('topiccollection', page_dictionaries, revision_id)


def page_dictionaries():
    return decamelize({
        'en': {
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
            }
        },
        'es': {
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
            }
        }
    })


# when importing the same page twice, we should just
# return the id of the previously imported page
@pytest.mark.django_db
def test_import_from_page_dictionary_twice():
    revision_id = 'UGFnZVJldmlzaW9uTm9kZToxMg=='

    # get the page we're creating
    page = create_topic_page_from_importer_dictionaries(page_dictionaries(), revision_id)

    # try making it again
    second_page = create_topic_page_from_importer_dictionaries(page_dictionaries(), revision_id)

    assert second_page == page
    # not sure if we need to check this or not so I'm checking it
    assert list(page.topic_collections.all()) == list(second_page.topic_collections.all())


# when importing the same page twice, with a different revision id
# we should just return the id of the previously imported page
# todo: decide if this is how we want this to work
@pytest.mark.django_db
def test_import_from_page_dictionary_twice_different_revisions():
    first_revision_id = 'first_revision_id'
    second_revision_id = 'second_revision_id'

    # get the page we're creating
    page = create_topic_page_from_importer_dictionaries(page_dictionaries(), first_revision_id)

    # try making it again
    second_page = create_topic_page_from_importer_dictionaries(page_dictionaries(), second_revision_id)

    assert second_page == page
    # not sure if we need to check this or not so I'm checking it
    assert list(page.topic_collections.all()) == list(second_page.topic_collections.all())


# when importing a page with an existing topic collection,
# we should use the existing theme for the page
@pytest.mark.django_db
def test_import_from_page_dictionary_existing_topic_collections():
    revision_id = 'UGFnZVJldmlzaW9uTm9kZToxMg=='
    topic_collection_page_revision_id = page_dictionaries()['en']['topiccollections']['edges'][0]['node']['topiccollection']['live_revision']['id']

    topic_collection_page_dictionaries = {
        'en': page_dictionaries()['en']['topiccollections']['edges'][0]['node']['topiccollection'],
        'es': page_dictionaries()['es']['topiccollections']['edges'][0]['node']['topiccollection']
    }
    topic_collection_pages = [create_topic_collection_page_from_importer_dictionaries(topic_collection_page_dictionaries, topic_collection_page_revision_id)]

    page = create_topic_page_from_importer_dictionaries(page_dictionaries(), revision_id)

    topic_collections_on_page = [base_page_topic_collection.topic_collection for base_page_topic_collection in page.topic_collections.all()]

    assert topic_collections_on_page == topic_collection_pages
