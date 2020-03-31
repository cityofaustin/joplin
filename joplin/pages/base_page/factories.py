import factory
from pages.factory import PageFactory

from pages.base_page.models import JanisBasePage
from pages.topic_page.models import JanisBasePageWithTopics, JanisBasePageTopic
from groups.factories import GroupPagePermissionFactory


class JanisBasePageFactory(PageFactory):
    class Meta:
        model = JanisBasePage

    @factory.post_generation
    def add_department(self, create, extracted, **kwargs):
        # TODO: add option to pass in already created departments
        if extracted:
            # A list of departments were passed in, use them
            # for related_department in extracted:
                # todo: add department stuff here
                # GroupPagePermissionFactory.create(page=self, topic_collection=topic_collection)
            return

        # pass "add_department__dummy"=True into Factory() to make dummy departments
        if create:
            if (kwargs.get("dummy", False)):
                GroupPagePermissionFactory.create(page=self)
