import factory
from pages.base_page.factories import JanisBasePageFactory
from pages.event_page.models import EventPage, EventPageFee
from pages.base_page.fixtures.helpers.streamfieldify import streamfieldify


class EventPageFactory(JanisBasePageFactory):
    class Meta:
        model = EventPage

    @classmethod
    def create(cls, *args, **kwargs):
        if 'location_blocks' in kwargs:
            kwargs['location_blocks'] = streamfieldify(kwargs['location_blocks'])
        return super(EventPageFactory, cls).create(*args, **kwargs)

    @factory.post_generation
    def add_fees(self, create, extracted, **kwargs):
        if extracted:
            # A list of topics were passed in, use them
            # reversed() to preserve insert order.
            for fee in reversed(extracted['fees']):
                EventPageFeeFactory.create(page=self, **fee)
            return


class EventPageFeeFactory(factory.DjangoModelFactory):
    page = factory.SubFactory(
        'event_page.factories.EventPageFactory'
    )

    class Meta:
        model = EventPageFee
