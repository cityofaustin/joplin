# Just commenting this one out for now, might have something useful in it for when we get to guide pages

# import factory
# import factory.fuzzy
# import wagtail_factories
# from django.utils.text import slugify
# from wagtail.core.models import Collection, Page
# from base.models import *
# from pages.service_page.models import ServicePage
# from pages.information_page.models import InformationPage
# from pages.topic_page.models import TopicPage
# from pages.guide_page.models import GuidePageTopic, GuidePageContact, GuidePage
# from wagtail.core import blocks
# from base.factories import PageFactory, TextBlockFactory
#
# """
# almost working
# might need to split page up into its own factory (pass page factory? choosing a page)
# or do more stuff in the build/create section to choose a random qualifying page
# """
#
#
# class SectionPageChooserBlockFactory(wagtail_factories.blocks.BlockFactory):
#     page = factory.fuzzy.FuzzyChoice([page for page in Page.objects.type(
#         tuple([ServicePage, InformationPage]))])
#
#     class Meta:
#         model = blocks.PageChooserBlock
#
#     @classmethod
#     def _build(cls, model_class, page):
#         return page
#
#     @classmethod
#     def _create(cls, model_class, page):
#         return page
#
#
# class GuidePageTopicFactory(factory.django.DjangoModelFactory):
#     page = factory.SubFactory('base.factories.guide_page.GuidePageFactory')
#     # TODO: make this factory, atm it chooses from existing topic pages
#     topic = factory.Iterator(TopicPage.objects.all())
#
#     class Meta:
#         model = GuidePageTopic
#
#
# class GuidePageContactFactory(factory.django.DjangoModelFactory):
#     page = factory.SubFactory('base.factories.guide_page.GuidePageFactory')
#     contact = factory.Iterator(Contact.objects.all())
#
#     class Meta:
#         model = GuidePageContact
#
#
# class GuidePageFactory(PageFactory):
#     description = factory.Faker('text')
#     image = factory.SubFactory(wagtail_factories.ImageFactory)
#     # sections = wagtail_factories.StreamFieldFactory()
#
#     class Meta:
#         model = GuidePage
#
#     @factory.post_generation
#     def create_related_objects(self, create, extracted, **kwargs):
#         if create:
#             GuidePageTopicFactory.create_batch(2, page=self)
#             GuidePageContactFactory.create_batch(2, page=self)
