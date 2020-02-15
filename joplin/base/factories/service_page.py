import factory
import wagtail_factories
from django.utils.text import slugify
from wagtail.core.models import Collection, Page
from base.models import *
from .base_factories import PageFactory


class ServicePageTopicFactory(factory.django.DjangoModelFactory):
    page = factory.SubFactory('base.factories.service_page.ServicePageFactory')
    # TODO: make this factory, atm it chooses from existing topic pages
    topic = factory.Iterator(TopicPage.objects.all())

    class Meta:
        model = ServicePageTopic


class ServicePageRelatedDepartmentsFactory(factory.django.DjangoModelFactory):
    page = factory.SubFactory('base.factories.service_page.ServicePageFactory')
    # TODO: make this factory
    related_department = factory.Iterator(DepartmentPage.objects.all())

    class Meta:
        model = ServicePageRelatedDepartments


class ServicePageContactFactory(factory.django.DjangoModelFactory):
    page = factory.SubFactory('base.factories.service_page.ServicePageFactory')
    # TODO: make this factory
    contact = factory.Iterator(Contact.objects.all())

    class Meta:
        model = ServicePageContact


class ServicePageFactory(PageFactory):
    steps = wagtail_factories.StreamFieldFactory(
        {'option': factory.Faker('text')}
    )
    dynamic_content = wagtail_factories.StreamFieldFactory(
        {'option': factory.Faker('text')}
    )
    additional_content = factory.Faker('text')
    short_description = factory.Faker('text')

    class Meta:
        model = ServicePage

    @factory.post_generation
    def create_related_objects(self, create, extracted, **kwargs):
        if create:
            ServicePageTopicFactory.create_batch(2, page=self)
            ServicePageRelatedDepartmentsFactory.create_batch(2, page=self)
            ServicePageContactFactory.create_batch(2, page=self)
