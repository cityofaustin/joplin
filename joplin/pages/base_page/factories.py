import factory
import wagtail_factories
from django.utils.text import slugify
from wagtail.core.models import Collection, Page, GroupPagePermission
from pages.factory import PageFactory
from pages.topic_page.factories import TopicPageFactory
from pages.home_page.factories import HomePageFactory

from pages.base_page.models import JanisBasePage
from pages.topic_page.models import JanisBasePageWithTopics, JanisBasePageTopic
from groups.factories import GroupPagePermissionFactory


class JanisBasePageFactory(PageFactory):
    class Meta:
        model = JanisBasePage

    @factory.post_generation
    def create_related_objects(self, create, extracted, **kwargs):
        if create:
            GroupPagePermissionFactory.create_batch(2, page=self)



class JanisBasePageTopicFactory(factory.django.DjangoModelFactory):
    page = factory.SubFactory('base_page.factories.JanisBasePageWithTopicsFactory')
    topic = factory.SubFactory(TopicPageFactory)

    class Meta:
        model = JanisBasePageTopic


class JanisBasePageWithTopicsFactory(JanisBasePageFactory):
    class Meta:
        model = JanisBasePageWithTopics

    @factory.post_generation
    def create_related_objects(self, create, extracted, **kwargs):
        if create:
            JanisBasePageTopicFactory.create_batch(2, page=self)
