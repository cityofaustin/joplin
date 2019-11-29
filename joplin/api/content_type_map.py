from base.models import (
    ServicePage,
    InformationPage,
    OfficialDocumentPage,
    GuidePage,
    FormContainer,
)

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
}
