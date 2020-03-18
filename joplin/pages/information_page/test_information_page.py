import pytest

# Try importing using dummy data in a page_dictionary
from pages.topic_collection_page.factories import ThemeFactory, TopicCollectionPageFactory, \
    create_topic_collection_page_from_page_dictionary
from pages.topic_page.factories import TopicPageFactory, create_topic_page_from_page_dictionary
from pages.information_page.factories import InformationPageFactory, create_information_page_from_page_dictionary


@pytest.mark.django_db
def test_import_dummy_data_from_page_dictionary():
    revision_id = 'UGFnZVJldmlzaW9uTm9kZToxMQ=='
    page_dictionary = {
        'id': 'SW5mb3JtYXRpb25QYWdlTm9kZTo2',
        'title': 'information page title [en]',
        'slug': 'information-page-title-en',
        'description': 'information page description [en]',
        'topics': {
            'edges': [{
                'node': {
                    'topic': {
                        'id': 'VG9waWNOb2RlOjU=',
                        'title': 'topic title [en]',
                        'slug': 'topic-title-en',
                        'description': 'topic description [en]',
                        'topiccollections': {
                            'edges': [{
                                'node': {
                                    'topiccollection': {
                                        'id': 'VG9waWNDb2xsZWN0aW9uTm9kZTo0',
                                        'title': 'topic collection title [en]',
                                        'slug': 'topic-collection-title-en',
                                        'description': 'topic collection description [en]',
                                        'theme': {
                                            'id': 'VGhlbWVOb2RlOjE=',
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
    }

    topic_page_dictionary = page_dictionary['topics']['edges'][0]['node']['topic']
    topic_page_revision_id = topic_page_dictionary['liveRevision']['id']

    topic_collection_page_dictionary = topic_page_dictionary['topiccollections']['edges'][0]['node']['topiccollection']
    topic_collection_page_revision_id = topic_collection_page_dictionary['liveRevision']['id']

    theme = ThemeFactory.build(slug=topic_collection_page_dictionary['theme']['slug'],
                               text=topic_collection_page_dictionary['theme']['text'],
                               description=topic_collection_page_dictionary['theme']['description'])

    assert theme.slug == topic_collection_page_dictionary['theme']['slug']
    assert theme.text == topic_collection_page_dictionary['theme']['text']
    assert theme.description == topic_collection_page_dictionary['theme']['description']

    topic_collection = TopicCollectionPageFactory.build(imported_revision_id=topic_collection_page_revision_id,
                                                        title=topic_collection_page_dictionary['title'],
                                                        slug=topic_collection_page_dictionary['slug'],
                                                        description=topic_collection_page_dictionary['description'],
                                                        theme=theme)

    assert topic_collection.title == topic_collection_page_dictionary['title']
    assert topic_collection.slug == topic_collection_page_dictionary['slug']
    assert topic_collection.description == topic_collection_page_dictionary['description']
    assert topic_collection.imported_revision_id == topic_collection_page_revision_id

    topic = TopicPageFactory.build(imported_revision_id=topic_page_revision_id, title=topic_page_dictionary['title'],
                                   slug=topic_page_dictionary['slug'],
                                   description=topic_page_dictionary['description'],
                                   topic_collections=[topic_collection])

    assert topic.title == topic_page_dictionary['title']
    assert topic.slug == topic_page_dictionary['slug']
    assert topic.description == topic_page_dictionary['description']
    assert topic.topic_collections.first() == topic_collection

    page = InformationPageFactory.build(imported_revision_id=revision_id, title=page_dictionary['title'],
                                        slug=page_dictionary['slug'], description=page_dictionary['description'],
                                        topics=[topic], additional_content=page_dictionary['additionalContent'],
                                        coa_global=page_dictionary['coaGlobal'])

    assert page.title == page_dictionary['title']
    assert page.slug == page_dictionary['slug']
    assert page.description == page_dictionary['description']
    assert page.topics.first() == topic
    assert page.additional_content == page_dictionary['additionalContent']
    assert page.coa_global == page_dictionary['coaGlobal']


# when importing the same page twice, we should just
# return the id of the previously imported page
@pytest.mark.django_db
def test_import_from_page_dictionary_twice():
    revision_id = 'UGFnZVJldmlzaW9uTm9kZToxMQ=='
    page_dictionary = {
        'id': 'SW5mb3JtYXRpb25QYWdlTm9kZTo2',
        'title': 'information page title [en]',
        'slug': 'information-page-title-en',
        'description': 'information page description [en]',
        'topics': {
            'edges': [{
                'node': {
                    'topic': {
                        'id': 'VG9waWNOb2RlOjU=',
                        'title': 'topic title [en]',
                        'slug': 'topic-title-en',
                        'description': 'topic description [en]',
                        'topiccollections': {
                            'edges': [{
                                'node': {
                                    'topiccollection': {
                                        'id': 'VG9waWNDb2xsZWN0aW9uTm9kZTo0',
                                        'title': 'topic collection title [en]',
                                        'slug': 'topic-collection-title-en',
                                        'description': 'topic collection description [en]',
                                        'theme': {
                                            'id': 'VGhlbWVOb2RlOjE=',
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
    }

    # get the page we're creating
    page = create_information_page_from_page_dictionary(page_dictionary, revision_id)

    # try making it again
    second_page = create_information_page_from_page_dictionary(page_dictionary, revision_id)

    assert second_page == page
    # not sure if we need to check this or not so I'm checking it
    assert list(page.topics.all()) == list(second_page.topics.all())
