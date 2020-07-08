from pages.service_page.models import ServicePage
from pages.information_page.models import InformationPage
from pages.official_documents_page.models import OfficialDocumentPage
from pages.guide_page.models import GuidePage
from pages.form_container.models import FormContainer
from pages.location_page.models import LocationPage
from pages.event_page.models import EventPage
from pages.topic_page.models import TopicPage
from pages.topic_collection_page.models import TopicCollectionPage
from pages.department_page.models import DepartmentPage
from pages.official_documents_collection.models import OfficialDocumentCollection

# Gain access to a content_type's node and model if you have it's name.
# Helps reduce copypasta in api.schema.py
# used in get_from_content_type and get_global_id_from_content_type
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
    },
    "topic page": {
        "node": "TopicNode",
        "model": TopicPage,
    },
    "topic collection page": {
        "node": "TopicCollectionNode",
        "model": TopicCollectionPage,
    },
    "department page": {
        "node": "DepartmentPageNode",
        "model": DepartmentPage,
    },
    "official document collection": {
        "node": "OfficialDocumentCollectionNode",
        "model": OfficialDocumentCollection
    }
}
