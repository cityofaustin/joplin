import factory
from pages.factory import PageFactory

from pages.base_page.models import JanisBasePage
from pages.topic_page.models import JanisBasePageWithTopics, JanisBasePageTopic
from groups.factories import GroupPagePermissionFactory


class JanisBasePageFactory(PageFactory):
    class Meta:
        model = JanisBasePage

    @factory.post_generation
    def add_related_departments(self, create, extracted, **kwargs):
        if extracted:
            # A list of departments were passed in, use them
            # for related_department in extracted:
                # todo: add department stuff here
                # GroupPagePermissionFactory.create(page=self, topic_collection=topic_collection)
            return

        # todo figure out if this is really what we want this factory to do
        if create:
            GroupPagePermissionFactory.create_batch(2, page=self)



# class JanisBasePageTopicFactory(factory.django.DjangoModelFactory):
#     page = factory.SubFactory('base_page.factories.JanisBasePageWithTopicsFactory')
#     topic = factory.SubFactory('pages.topic_page.factories.TopicPageFactory')
#
#     class Meta:
#         model = JanisBasePageTopic
#
#
# class JanisBasePageWithTopicsFactory(JanisBasePageFactory):
#     class Meta:
#         model = JanisBasePageWithTopics
#
#     @factory.post_generation
#     def create_parent_topics(self, create, extracted, **kwargs):
#         if create:
#             JanisBasePageTopicFactory.create_batch(2, page=self)
