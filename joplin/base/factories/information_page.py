import factory
import wagtail_factories
from django.utils.text import slugify
from base.models import *
from . import PageFactory
from pytest_factoryboy import register


class InformationPageTopicFactory(factory.django.DjangoModelFactory):
    page = factory.SubFactory('base.factories.information_page.InformationPageFactory')
    # TODO: make this factory, atm it chooses from existing topic pages
    topic = factory.Iterator(TopicPage.objects.all())

    class Meta:
        model = InformationPageTopic


# TODO: reimplement with new model
# class InformationPageRelatedDepartmentsFactory(factory.django.DjangoModelFactory):
#     page = factory.SubFactory('base.factories.information_page.InformationPageFactory')
#     # TODO: make this factory
#     related_department = factory.Iterator(DepartmentPage.objects.all())
#
#     class Meta:
#         model = InformationPageRelatedDepartments


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
            # TODO: reimplement with new model
            # InformationPageRelatedDepartmentsFactory.create_batch(2, page=self)
            InformationPageContactFactory.create_batch(2, page=self)
