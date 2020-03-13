import factory
from pages.factory import PageFactory

from pages.base_page.models import JanisBasePage
from pages.topic_page.models import JanisBasePageWithTopics, JanisBasePageTopic
from groups.factories import GroupPagePermissionFactory


class JanisBasePageFactory(PageFactory):
    class Meta:
        model = JanisBasePage

    @factory.post_generation
    def create_related_departments(self, create, extracted, **kwargs):
        if create:
            GroupPagePermissionFactory.create_batch(2, page=self)


class JanisBasePageTopicFactory(factory.django.DjangoModelFactory):
    page = factory.SubFactory('base_page.factories.JanisBasePageWithTopicsFactory')
    topic = factory.SubFactory('pages.topic_page.factories.TopicPageFactory')

    class Meta:
        model = JanisBasePageTopic


class JanisBasePageWithTopicsFactory(JanisBasePageFactory):
    class Meta:
        model = JanisBasePageWithTopics

    @factory.post_generation
    def create_parent_topics(self, create, extracted, **kwargs):
        if create:
            JanisBasePageTopicFactory.create_batch(2, page=self)
