import factory
import wagtail_factories
from django.utils.text import slugify
from wagtail.core.models import Collection, Page
from . import models


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


class LocationFactory(factory.django.DjangoModelFactory):
    full_address = factory.Faker('address')
    unit_number = factory.Faker('random_int')
    geography = factory.Faker('local_latlng')

    class Meta:
        model = models.Location


class PhysicalAddressFactory(factory.django.DjangoModelFactory):
    full_address = factory.Faker('address')
    unit_number = factory.Faker('random_int')
    geography = factory.Faker('local_latlng')

    location_photo = factory.SubFactory(wagtail_factories.ImageFactory)

    class Meta:
        model = models.PhysicalAddress


class LocationPageFactory(PageFactory):

    primary_name = factory.Faker('text')
    alternate_name = factory.Faker('text')
    physical_address = factory.SubFactory(PhysicalAddressFactory)
    mailing_address = factory.SubFactory(LocationFactory)

    class Meta:
        model = models.LocationPage
