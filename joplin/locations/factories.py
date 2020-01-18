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

class LocationPageRelatedServicesFactory(factory.django.DjangoModelFactory):
    # find all your fields [f.name for f in MyModel._meta.get_fields()]
    page = factory.RelatedFactory('factories.LocationPageFactory')
    hours_exceptions = factory.Faker('text')
    # TODO: figure out how to call method/programatically generate these fields
    # for day in ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]:
    #     print(day)
    #     day_start_field = '%s_start_time' % day.lower()
    #     day_end_field = '%s_end_time' % day.lower()
    #     day_open_field = '%s_open' % day.lower()
    #     day_start_field = factory.Faker('time', pattern="%H:%M", end_datetime=None)
    #     day_end_field = factory.Faker('time', pattern="%H:%M", end_datetime=None)

    # (day_start_field + "_2") = factory.Faker('time', pattern="%H:%M", end_datetime=None)
    # (day_end_field + "_2") = factory.Faker('time', pattern="%H:%M", end_datetime=None)

    class Meta:
        model = models.LocationPageRelatedServices

class LocationPageFactory(PageFactory):
    alternate_name = factory.Faker('text')

    physical_street = factory.Faker('street_address')
    physical_unit = factory.Faker('secondary_address')
    physical_city = factory.Faker('city')
    physical_state = factory.Faker('state_abbr')
    physical_country = factory.Faker('country_code')
    physical_zip = factory.Faker('zipcode_in_state')

    physical_location_photo = factory.SubFactory(wagtail_factories.ImageFactory)

    mailing_street = factory.Faker('street_address')
    mailing_city = factory.Faker('city')
    mailing_state = factory.Faker('state_abbr')
    mailing_country = factory.Faker('country_code')
    mailing_zip = factory.Faker('zipcode_in_state')

    nearest_bus_1 = factory.Faker('random_int', min=0, max=999, step=1)
    nearest_bus_2 = factory.Faker('random_int', min=0, max=999, step=1)
    nearest_bus_3 = factory.Faker('random_int', min=0, max=999, step=1)

    related_services = factory.SubFactory(LocationPageRelatedServicesFactory)

    class Meta:
        model = models.LocationPage
