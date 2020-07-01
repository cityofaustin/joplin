import factory
from pages.official_documents_page_new.models import OfficialDocumentPageNew
from pages.base_page.factories import JanisBasePageFactory
from wagtail.documents.models import Document


class DocumentFactory(factory.DjangoModelFactory):
    @classmethod
    def create(cls, *args, **kwargs):
        return super(DocumentFactory, cls).create(*args, **kwargs)

    class Meta:
        model = Document


class OfficialDocumentPageNewFactory(JanisBasePageFactory):
    class Meta:
        model = OfficialDocumentPageNew

    document = factory.SubFactory(
        DocumentFactory
    )

    # Todo: add this?
    # @factory.post_generation
    # def add_official_documents(self, create, extracted, **kwargs):
    #     if extracted:
    #         # A list of documents were passed in, use them
    #         # reversed() to preserve insert order.
    #         for official_documents_page_document in reversed(extracted['official_documents_page_documents']):
    #             OfficialDocumentPageDocumentFactory.create(page=self, **official_documents_page_document)
    #         return
