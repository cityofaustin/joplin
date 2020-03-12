import factory
import wagtail_factories
from django.utils.text import slugify
from wagtail.core.models import Collection, Page
from pages.factory import PageFactory
from pages.topic_page.factories import TopicPageFactory

from pages.base_page.models import JanisBasePage
from pages.topic_page.models import JanisBasePageWithTopics, JanisBasePageTopic


class JanisBasePageFactory(PageFactory):
    class Meta:
        model = JanisBasePage


class JanisBasePageTopicFactory(factory.django.DjangoModelFactory):
    page = factory.SubFactory('base_page.factories.JanisBasePageWithTopicsFactory')
    topic = TopicPageFactory(parent=home_page)

    class Meta:
        model = JanisBasePageTopic


class JanisBasePageWithTopicsFactory(JanisBasePageFactory):
    class Meta:
        model = JanisBasePageWithTopics

    @factory.post_generation
    def create_related_objects(self, create, extracted, **kwargs):
        if create:
            JanisBasePageTopicFactory.create_batch(2, page=self)
