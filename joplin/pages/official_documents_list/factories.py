from pages.official_documents_list.models import OfficialDocumentList
from pages.topic_page.factories import JanisBasePageWithTopicsFactory


class OfficialDocumentListFactory(JanisBasePageWithTopicsFactory):
    class Meta:
        model = OfficialDocumentList
