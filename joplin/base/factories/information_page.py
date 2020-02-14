import factory
import wagtail_factories
from django.utils.text import slugify
from wagtail.core.models import Collection, Page
from base.models import *


class PageFactory(wagtail_factories.factories.MP_NodeFactory):
    """
    little hack from wagtail_factories cause I don't want a hard-coded page title
    note: when creating pages give it a parent (parent=<another page like home page>)
    or else it'l be an orphan and you'll both be sad
    """
    title = factory.Faker('text')
    slug = factory.LazyAttribute(lambda obj: slugify(obj.title))

    class Meta:
        model = Page


class InformationPageTopicFactory(factory.django.DjangoModelFactory):
    page = factory.SubFactory('base.factories.information_page.InformationPageFactory')
    # TODO: make this factory, atm it chooses from existing topic pages
    topic = factory.Iterator(TopicPage.objects.all())

    class Meta:
        model = InformationPageTopic


class InformationPageRelatedDepartmentsFactory(factory.django.DjangoModelFactory):
    page = factory.SubFactory('base.factories.information_page.InformationPageFactory')
    # TODO: make this factory
    related_department = factory.Iterator(DepartmentPage.objects.all())

    class Meta:
        model = InformationPageRelatedDepartments


class InformationPageContactFactory(factory.django.DjangoModelFactory):
    page = factory.SubFactory('base.factories.information_page.InformationPageFactory')
    # TODO: make this factory
    contact = factory.Iterator(Contact.objects.all())

    class Meta:
        model = InformationPageContact


class InformationPageFactory(PageFactory):
    description = factory.Faker('text')
    options = wagtail_factories.StreamFieldFactory(
        {'option': factory.Faker('text')}
    )
    additional_content = factory.Faker('text')

    class Meta:
        model = InformationPage

    @factory.post_generation
    def create_related_objects(self, create, extracted, **kwargs):
        if create:
            InformationPageTopicFactory.create_batch(2, page=self)
            InformationPageRelatedDepartmentsFactory.create_batch(2, page=self)
            InformationPageContactFactory.create_batch(2, page=self)
