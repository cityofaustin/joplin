import factory
from pages.topic_collection_page.models import TopicCollectionPage, JanisBasePageTopicCollection, JanisBasePageWithTopicCollections
from pages.base_page.factories import JanisBasePageFactory
from pages.factory import PageFactory


class TopicCollectionPageFactory(PageFactory):

    class Meta:
        model = TopicCollectionPage


class JanisBasePageTopicCollectionFactory(factory.django.DjangoModelFactory):
    page = factory.SubFactory('base_page.factories.JanisBasePageWithTopicsFactory')
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
