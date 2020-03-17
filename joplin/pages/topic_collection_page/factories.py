import factory
from pages.topic_collection_page.models import TopicCollectionPage, JanisBasePageTopicCollection, JanisBasePageWithTopicCollections
from pages.base_page.factories import JanisBasePageFactory
from pages.factory import PageFactory
from base.models import Theme


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
    def create_related_objects(self, create, extracted, **kwargs):
        if create:
            JanisBasePageTopicCollectionFactory.create_batch(2, page=self)
