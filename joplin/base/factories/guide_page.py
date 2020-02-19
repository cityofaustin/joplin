import factory
import factory.fuzzy
import wagtail_factories
from django.utils.text import slugify
from wagtail.core.models import Collection, Page
from base.models import *
from wagtail.core import blocks
from .base_factories import PageFactory


class PageChooserBlockFactory(wagtail_factories.blocks.BlockFactory):
    page = factory.fuzzy.FuzzyChoice([page for page in Page.objects.type(
        tuple([ServicePage, InformationPage]))])

    class Meta:
        model = blocks.PageChooserBlock

    @classmethod
    def _build(cls, model_class, page):
        return page

    @classmethod
    def _create(cls, model_class, page):
        return page


class GuidePageTopicFactory(factory.django.DjangoModelFactory):
    page = factory.SubFactory('base.factories.guide_page.GuidePageFactory')
    # TODO: make this factory, atm it chooses from existing topic pages
    topic = factory.Iterator(TopicPage.objects.all())

    class Meta:
        model = GuidePageTopic


class GuidePageRelatedDepartmentsFactory(factory.django.DjangoModelFactory):
    page = factory.SubFactory('base.factories.guide_page.GuidePageFactory')

    related_department = factory.Iterator(DepartmentPage.objects.all())

    class Meta:
        model = GuidePageRelatedDepartments


class GuidePageContactFactory(factory.django.DjangoModelFactory):
    page = factory.SubFactory('base.factories.guide_page.GuidePageFactory')
    contact = factory.Iterator(Contact.objects.all())

    class Meta:
        model = GuidePageContact


class SectionFactory(wagtail_factories.StructBlockFactory):
    section_heading_en = factory.Faker('text')
    # TODO: making the streamfield factory work is gonna be a thing
    pages = wagtail_factories.ListBlockFactory(PageChooserBlockFactory)


class GuidePageFactory(PageFactory):
    description = factory.Faker('text')
    image = factory.SubFactory(wagtail_factories.ImageFactory)
    sections = wagtail_factories.StreamFieldFactory(
        {'section': wagtail_factories.StructBlockFactory}
    )

    class Meta:
        model = GuidePage

    @factory.post_generation
    def create_related_objects(self, create, extracted, **kwargs):
        if create:
            GuidePageTopicFactory.create_batch(2, page=self)
            GuidePageRelatedDepartmentsFactory.create_batch(2, page=self)
            GuidePageContactFactory.create_batch(2, page=self)
