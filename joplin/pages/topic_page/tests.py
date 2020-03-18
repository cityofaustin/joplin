import pytest

# Try importing using dummy data in a page_dictionary
from pages.topic_collection_page.factories import ThemeFactory, TopicCollectionPageFactory
from pages.topic_page.factories import TopicPageFactory, create_topic_page_from_page_dictionary


@pytest.mark.django_db
def test_import_dummy_data_from_page_dictionary():
    revision_id = 'UGFnZVJldmlzaW9uTm9kZToxMg=='
    page_dictionary = {
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
        }
    }

    topic_collection_page_dictionary = page_dictionary['topiccollections']['edges'][0]['node']['topiccollection']
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

    page = TopicPageFactory.build(imported_revision_id=revision_id, title=page_dictionary['title'],
                                  slug=page_dictionary['slug'],
                                  description=page_dictionary['description'],
                                  topic_collections=[topic_collection])

    assert page.title == page_dictionary['title']
    assert page.slug == page_dictionary['slug']
    assert page.description == page_dictionary['description']
    assert page.topic_collections.first() == topic_collection


# when importing the same page twice, we should just
# return the id of the previously imported page
@pytest.mark.django_db
def test_import_from_page_dictionary_twice():
    revision_id = 'UGFnZVJldmlzaW9uTm9kZToxMg=='
    page_dictionary = {
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
        }
    }

    # get the page we're creating
    page = create_topic_page_from_page_dictionary(page_dictionary, revision_id)

    # try making it again
    second_page = create_topic_page_from_page_dictionary(page_dictionary, revision_id)

    assert second_page == page

#
# # when importing the same page twice, with a different revision id
# # we should just return the id of the previously imported page
# # todo: decide if this is how we want this to work
# @pytest.mark.django_db
# def test_import_from_page_dictionary_twice_different_revisions():
#     first_revision_id = 'first_revision_id'
#     second_revision_id = 'second_revision_id'
#     page_dictionary = {
#         'id': 'VG9waWNDb2xsZWN0aW9uTm9kZTo0',
#         'title': 'topic collection title [en]',
#         'slug': 'topic-collection-title-en',
#         'description': 'topic collection description [en]',
#         'theme': {
#             'id': 'VGhlbWVOb2RlOjE=',
#             'slug': 'theme-slug-en',
#             'text': 'theme text [en]',
#             'description': 'theme description [en]'
#         }
#     }
#
#     # get the page we're creating
#     page = create_topic_collection_page_from_page_dictionary(page_dictionary, first_revision_id)
#
#     # try making it again
#     second_page = create_topic_collection_page_from_page_dictionary(page_dictionary, second_revision_id)
#
#     assert second_page == page
#
#
# # when importing a page with an existing theme,
# # we should use the existing theme for the page
# @pytest.mark.django_db
# def test_import_from_page_dictionary_existing_theme():
#     revision_id = 'UGFnZVJldmlzaW9uTm9kZToxMw=='
#     page_dictionary = {
#         'id': 'VG9waWNDb2xsZWN0aW9uTm9kZTo0',
#         'title': 'topic collection title [en]',
#         'slug': 'topic-collection-title-en',
#         'description': 'topic collection description [en]',
#         'theme': {
#             'id': 'VGhlbWVOb2RlOjE=',
#             'slug': 'theme-slug-en',
#             'text': 'theme text [en]',
#             'description': 'theme description [en]'
#         }
#     }
#
#     theme = ThemeFactory.create(slug=page_dictionary['theme']['slug'], text=page_dictionary['theme']['text'],
#                                 description=page_dictionary['theme']['description'])
#
#     page = create_topic_collection_page_from_page_dictionary(page_dictionary, revision_id)
#
#     assert page.theme == theme
