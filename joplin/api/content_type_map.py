from pages.service_page.models import ServicePage
from pages.information_page.models import InformationPage
from pages.official_documents_page.models import OfficialDocumentPage
from pages.guide_page.models import GuidePage
from pages.form_container.models import FormContainer

from locations.models import LocationPage
from events.models import EventPage

# Gain access to a content_type's node and model if you have it's name.
# Helps reduce copypasta in api.schema.py
content_type_map = {
    "service page": {
        "node": "ServicePageNode",
        "model": ServicePage,
    },
    "information page": {
        "node": "InformationPageNode",
        "model": InformationPage,
    },
    "official document page": {
        "node": "OfficialDocumentPageNode",
        "model": OfficialDocumentPage,
    },
    "guide page": {
        "node": "GuidePageNode",
        "model": GuidePage,
    },
    "form container": {
        "node": "FormContainerNode",
        "model": FormContainer,
    },
    "location page": {
        "node": "LocationPageNode",
        "model": LocationPage
    },
    "event page": {
        "node": "EventPageNode",
        "model": EventPage
    }
}
