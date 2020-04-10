from pages.base_page.factories import JanisBasePageFactory
from pages.event_page.models import EventPage

class EventPageFactory(JanisBasePageFactory):
    class Meta:
        model = EventPage
