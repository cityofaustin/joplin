import factory
from pages.topic_collection_page.models import TopicCollectionPage, JanisBasePageTopicCollection, JanisBasePageWithTopicCollections
from pages.base_page.factories import JanisBasePageFactory
from snippets.theme.models import Theme


class ThemeFactory(factory.django.DjangoModelFactory):
    slug = 'theme_slug'

    class Meta:
        model = Theme


class TopicCollectionPageFactory(JanisBasePageFactory):
    theme = factory.SubFactory(ThemeFactory)

    class Meta:
        model = TopicCollectionPage


class JanisBasePageTopicCollectionFactory(factory.django.DjangoModelFactory):
    page = factory.SubFactory(
        'base_page.factories.JanisBasePageWithTopicCollectionsFactory',
        add_department__dummy=True
    )
    topic_collection = factory.SubFactory(
        TopicCollectionPageFactory,
        add_department__dummy=True
    )

    class Meta:
        model = JanisBasePageTopicCollection


class JanisBasePageWithTopicCollectionsFactory(JanisBasePageFactory):
    class Meta:
        model = JanisBasePageWithTopicCollections

    @factory.post_generation
    def add_topic_collections(self, create, extracted, **kwargs):
        if extracted:
            # A list of topic collections were passed in, use them
            for topic_collection in extracted['topic_collections']:
                # todo: check to see if we already have the basepagetopiccollection objects made
                JanisBasePageTopicCollectionFactory.create(page=self, topic_collection=topic_collection)
            return

        # todo figure out if this is really what we want this factory to do
        if create:
            JanisBasePageTopicCollectionFactory.create_batch(2, page=self)
