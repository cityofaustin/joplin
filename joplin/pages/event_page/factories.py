from pages.base_page.factories import JanisBasePageFactory
from pages.event_page.models import EventPage
from pages.base_page.fixtures.helpers.streamfieldify import streamfieldify


class EventPageFactory(JanisBasePageFactory):
    class Meta:
        model = EventPage


    @classmethod
    def create(cls, *args, **kwargs):
        # TODO handle fees
        if 'fees' in kwargs:
            del kwargs['fees']
        if 'location_blocks' in kwargs:
            kwargs['location_blocks'] = streamfieldify(kwargs['location_blocks'])
        return super(EventPageFactory, cls).create(*args, **kwargs)
