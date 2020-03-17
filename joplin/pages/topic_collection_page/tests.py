from pages.topic_collection_page.factories import TopicCollectionPageFactory, JanisBasePageWithTopicCollectionsFactory, \
    ThemeFactory
import pytest


# If we don't have a theme
@pytest.mark.django_db
def test_topic_collection_page_no_theme_urls():
    page = TopicCollectionPageFactory.build(slug="topic_collection_slug")

    # by default the factory makes a theme for our topic collections,
    # so let's clear it out here
    page.theme.slug = None

    urls = page.janis_urls()
    url = page.janis_url()

    assert urls == []
    assert url == '#'


# If we have a theme
@pytest.mark.django_db
def test_topic_collection_page_with_theme_urls():
    page = TopicCollectionPageFactory.create(slug="topic_collection_slug")

    urls = page.janis_urls()
    url = page.janis_url()

    assert urls == ['http://fake.base.url/theme_slug/topic_collection_slug/']
    assert url == 'http://fake.base.url/theme_slug/topic_collection_slug/'


# If we don't have a topic collection
@pytest.mark.django_db
def test_janis_page_with_topic_collections_no_urls():
    page = JanisBasePageWithTopicCollectionsFactory.build(slug="page_slug")

    urls = page.janis_urls()
    url = page.janis_url()

    assert urls == []
    assert url == '#'


# If we have topic collections
@pytest.mark.django_db
def test_janis_page_with_topic_collections_urls():
    page = JanisBasePageWithTopicCollectionsFactory.create(slug="page_slug")
    topic_collections = [base_page_topic_collection.topic_collection for base_page_topic_collection in
                         page.topic_collections.all()]

    urls = page.janis_urls()
    url = page.janis_url()

    expected_urls = ['http://fake.base.url/theme_slug/{topic_collection_slug}/page_slug/'.format(
        topic_collection_slug=topic_collection.slug) for topic_collection in topic_collections]

    assert urls == expected_urls
    assert url == expected_urls[0]


# Try importing using dummy data in a page_dictionary
@pytest.mark.django_db
def test_import_dummy_data_from_page_dictionary():
    revision_id = 'UGFnZVJldmlzaW9uTm9kZToxMw=='
    page_dictionary = {
        'id': 'VG9waWNDb2xsZWN0aW9uTm9kZTo0',
        'title': 'topic collection title [en]',
        'slug': 'topic-collection-title-en',
        'description': 'topic collection description [en]',
        'theme': {
            'id': 'VGhlbWVOb2RlOjE=',
            'slug': 'theme-slug-en',
            'text': 'theme text [en]',
            'description': 'theme description [en]'
        }
    }

    theme = ThemeFactory.build(slug=page_dictionary['theme']['slug'], text=page_dictionary['theme']['text'], description=page_dictionary['theme']['description'])

    assert theme.slug == page_dictionary['theme']['slug']
    assert theme.text == page_dictionary['theme']['text']
    assert theme.description == page_dictionary['theme']['description']

    page = TopicCollectionPageFactory.build(imported_revision_id=revision_id, title=page_dictionary['title'],
                                            slug=page_dictionary['slug'], description=page_dictionary['description'],
                                            theme=theme)

    assert page.title == page_dictionary['title']
    assert page.slug == page_dictionary['slug']
    assert page.description == page_dictionary['description']
    assert page.imported_revision_id == revision_id
