from pages.topic_collection_page.factories import TopicCollectionPageFactory, JanisBasePageWithTopicCollectionsFactory, \
    ThemeFactory, create_topic_collection_page_from_importer_dictionaries, create_theme_from_importer_dictionaries
import pytest


def page_dictionaries():
    return {
        'en': {
            'title': 'topic collection title [en]',
            'slug': 'topic-collection-title-en',
            'description': 'topic collection description [en]',
            'theme': {
                'slug': 'theme-slug-en',
                'text': 'theme text [en]',
                'description': 'theme description [en]'
            }
        },
        'es': {
            'title': 'topic collection title [es]',
            'slug': 'topic-collection-title-es',
            'description': 'topic collection description [es]',
            'theme': {
                'slug': 'theme-slug-es',
                'text': 'theme text [es]',
                'description': 'theme description [es]'
            }
        }
    }


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



# when importing the same page twice, we should just
# return the id of the previously imported page
@pytest.mark.django_db
def test_import_from_page_dictionary_twice():
    revision_id = 'UGFnZVJldmlzaW9uTm9kZToxMw=='

    # get the page we're creating
    page = create_topic_collection_page_from_importer_dictionaries(page_dictionaries(), revision_id)

    # try making it again
    second_page = create_topic_collection_page_from_importer_dictionaries(page_dictionaries(), revision_id)

    assert second_page == page


# when importing the same page twice, with a different revision id
# we should just return the id of the previously imported page
# todo: decide if this is how we want this to work
@pytest.mark.django_db
def test_import_from_page_dictionary_twice_different_revisions():
    first_revision_id = 'first_revision_id'
    second_revision_id = 'second_revision_id'

    # get the page we're creating
    page = create_topic_collection_page_from_importer_dictionaries(page_dictionaries(), first_revision_id)

    # try making it again
    second_page = create_topic_collection_page_from_importer_dictionaries(page_dictionaries(), second_revision_id)

    assert second_page == page

# when importing a page with an existing theme,
# we should use the existing theme for the page
@pytest.mark.django_db
def test_import_from_page_dictionary_existing_theme():
    revision_id = 'UGFnZVJldmlzaW9uTm9kZToxMw=='

    theme_dictionaries = {
        'en': page_dictionaries()['en']['theme'],
        'es': page_dictionaries()['es']['theme']
    }
    theme = create_theme_from_importer_dictionaries(theme_dictionaries)

    page = create_topic_collection_page_from_importer_dictionaries(page_dictionaries(), revision_id)

    assert page.theme == theme
