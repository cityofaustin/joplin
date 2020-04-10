import factory
from pages.base_page.factories import JanisBasePageFactory
from pages.location_page.models import LocationPage, LocationPageRelatedServices


class LocationPageRelatedServicesFactory(factory.django.DjangoModelFactory):
    page = factory.SubFactory('pages.location_page.factories.LocationPageFactory')
    related_service = factory.SubFactory('pages.service_page.factories.ServicePageFactory')

    class Meta:
        model = LocationPageRelatedServices


class LocationPageFactory(JanisBasePageFactory):
    @classmethod
    def create(cls, *args, **kwargs):
        return super(LocationPageFactory, cls).create(*args, **kwargs)

    @factory.post_generation
    def add_related_services(self, create, extracted, **kwargs):
        if extracted:
            # A list of related services were passed in,
            # this includes info about hours for the related service
            for location_page_related_service in extracted:
                LocationPageRelatedServicesFactory.create(page=self, **location_page_related_service)
            return

    class Meta:
        model = LocationPage
