from pages.official_documents_collection.models import OfficialDocumentCollection
from pages.topic_page.factories import JanisBasePageWithTopicsFactory


class OfficialDocumentListFactory(JanisBasePageWithTopicsFactory):
    class Meta:
        model = OfficialDocumentCollection
