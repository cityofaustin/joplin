import factory
from pages.topic_page.models import TopicPage, JanisBasePageTopic, JanisBasePageWithTopics, TopicPageTopPage
from pages.topic_collection_page.factories import JanisBasePageWithTopicCollectionsFactory
from pages.base_page.factories import JanisBasePageFactory


class TopicPageFactory(JanisBasePageWithTopicCollectionsFactory):
    class Meta:
        model = TopicPage


class TopicPageTopPageFactory(factory.django.DjangoModelFactory):
    topic = factory.SubFactory('pages.topic_page.factories.TopicPageFactory')
    page = factory.SubFactory('base_page.factories.JanisBasePageWithTopicsFactory')

    class Meta:
        model = TopicPageTopPage


class JanisBasePageTopicFactory(factory.django.DjangoModelFactory):
    page = factory.SubFactory(
        'base_page.factories.JanisBasePageWithTopicsFactory',
        add_departments__dummy=True,
    )
    topic = factory.SubFactory(
        TopicPageFactory,
        add_departments__dummy=True,
    )

    class Meta:
        model = JanisBasePageTopic


class JanisBasePageWithTopicsFactory(JanisBasePageFactory):
    class Meta:
        model = JanisBasePageWithTopics

    @factory.post_generation
    def add_topics(self, create, extracted, **kwargs):
        # TODO: add option to pass in already created topics
        if extracted:
            # A list of topics were passed in, use them
            for topic in extracted['topics']:
                # todo: check to see if we already have the basepagetopiccollection objects made
                JanisBasePageTopicFactory.create(page=self, topic=topic)
            return

        # pass "add_topics__dummy"=True into Factory() to make dummy topics
        if create:
            if (kwargs.get("dummy", False)):
                JanisBasePageTopicFactory.create_batch(2, page=self)
