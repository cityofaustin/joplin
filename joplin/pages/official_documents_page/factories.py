import factory
from pages.official_documents_page.models import OfficialDocumentPage, OfficialDocumentPageDocument
from pages.topic_page.factories import JanisBasePageWithTopicsFactory
from wagtail.documents.models import Document


class OfficialDocumentPageFactory(JanisBasePageWithTopicsFactory):
    class Meta:
        model = OfficialDocumentPage

    @factory.post_generation
    def add_official_documents_page_documents(self, create, extracted, **kwargs):
        if extracted:
            # A list of topics were passed in, use them
            for official_documents_page_document in extracted['official_documents_page_documents']:
                OfficialDocumentPageDocumentFactory.create(page=self, **official_documents_page_document)
            return


class DocumentFactory(factory.DjangoModelFactory):
    @classmethod
    def create(cls, *args, **kwargs):
        return super(DocumentFactory, cls).create(*args, **kwargs)

    class Meta:
        model = Document


class OfficialDocumentPageDocumentFactory(factory.DjangoModelFactory):
    page = factory.SubFactory(
        'official_documents_page.factories.OfficialDocumentsPageFactory',
    )

    document = factory.SubFactory(
        DocumentFactory
    )

    class Meta:
        model = OfficialDocumentPageDocument
