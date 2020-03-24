import factory
from pages.topic_collection_page.models import TopicCollectionPage, JanisBasePageTopicCollection, JanisBasePageWithTopicCollections
from pages.base_page.factories import JanisBasePageFactory
from pages.factory import PageFactory
from pages.home_page.models import HomePage
from base.models import Theme
from wagtail.core.models import Page


class ThemeFactory(factory.django.DjangoModelFactory):
    slug = 'theme_slug'

    class Meta:
        model = Theme


class TopicCollectionPageFactory(PageFactory):
    theme = factory.SubFactory(ThemeFactory)

    class Meta:
        model = TopicCollectionPage


class JanisBasePageTopicCollectionFactory(factory.django.DjangoModelFactory):
    page = factory.SubFactory('base_page.factories.JanisBasePageWithTopicCollectionsFactory')
    topic_collection = factory.SubFactory(TopicCollectionPageFactory)

    class Meta:
        model = JanisBasePageTopicCollection


class JanisBasePageWithTopicCollectionsFactory(JanisBasePageFactory):
    class Meta:
        model = JanisBasePageWithTopicCollections

    @factory.post_generation
    def add_topic_collections(self, create, extracted, **kwargs):
        if extracted:
            # A list of topic collections were passed in, use them
            for topic_collection in extracted:
                # todo: check to see if we already have the basepagetopiccollection objects made
                JanisBasePageTopicCollectionFactory.create(page=self, topic_collection=topic_collection)
            return

        # todo figure out if this is really what we want this factory to do
        if create:
            JanisBasePageTopicCollectionFactory.create_batch(2, page=self)


def create_theme_from_importer_dictionaries(theme_dictionaries):
    # todo: use something other than slug here
    # todo: add imported id to themes
    try:
        theme = Theme.objects.get(slug=theme_dictionaries['en']['slug'])
        return theme
    except Theme.DoesNotExist:
        theme = None
    if not theme:
        combined_dictionary = theme_dictionaries['en']
        for field in ThemeFactory._meta.model._meta.fields:
            if field.column.endswith("_es"):
                combined_dictionary[field.column] = theme_dictionaries['es'][field.column[:-3]]

        return ThemeFactory.create(**combined_dictionary)


def create_topic_collection_page_from_importer_dictionaries(page_dictionaries, revision_id):
    # first check to see if we already imported this page
    # if we did, just go to the edit page for it without changing the db
    # todo: maybe change this to allow updating pages in the future?
    try:
        page = TopicCollectionPage.objects.get(imported_revision_id=revision_id)
    except TopicCollectionPage.DoesNotExist:
        page = None
    if page:
        return page

    # since we don't have a page matching the revision id, we should look
    # for other matches, for now let's just use the english slug
    # todo: figure out what we want the logic around importing a page with the same slug to look like
    try:
        page = TopicCollectionPage.objects.get(slug=page_dictionaries['en']['slug'])
    except TopicCollectionPage.DoesNotExist:
        page = None
    if page:
        return page

    # since we don't have a page matching the revision id or the slug
    # make the combined page dictionary
    combined_dictionary = page_dictionaries['en']

    # remove liveRevision if we have it
    # todo: why isn't pop working?
    if 'liveRevision' in combined_dictionary:
        del combined_dictionary['liveRevision']

    # set the revision id
    combined_dictionary['imported_revision_id'] = revision_id

    # set the theme
    # todo: not hardcode langs in here
    combined_dictionary['theme'] = create_theme_from_importer_dictionaries({'en': page_dictionaries['en']['theme'], 'es': page_dictionaries['es']['theme']})

    # Set home as parent
    # todo: move this to base page factory?
    combined_dictionary['parent'] = HomePage.objects.first()

    # set the translated fields
    for field in TopicCollectionPageFactory._meta.model._meta.fields:
        if field.column.endswith("_es"):
            if field.column[:-3] in page_dictionaries['es']:
                combined_dictionary[field.column] = page_dictionaries['es'][field.column[:-3]]

    # create the page
    return TopicCollectionPageFactory.create(**combined_dictionary)
