import factory
from pages.official_documents_page_new.models import OfficialDocumentPageNew
from pages.base_page.factories import JanisBasePageFactory
from pages.official_documents_collection.factories import OfficialDocumentCollectionFactory
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

    @factory.post_generation
    def add_official_document_collection(self, create, extracted, **kwargs):
        if extracted:
            # A list of official document collections were passed in, use them
            for collection in extracted['official_document_collection']:
                # todo: check to see if we already have the basepagetopiccollection objects made
                OfficialDocumentCollectionFactory.create(page=self, official_document_collection=collection)
            return

        # pass "add_topics__dummy"=True into Factory() to make dummy document collections
        if create:
            if kwargs.get("dummy", False):
                OfficialDocumentCollectionFactory.create_batch(2, page=self)


    # Todo: add this?
    # @factory.post_generation
    # def add_official_documents(self, create, extracted, **kwargs):
    #     if extracted:
    #         # A list of documents were passed in, use them
    #         # reversed() to preserve insert order.
    #         for official_documents_page_document in reversed(extracted['official_documents_page_documents']):
    #             OfficialDocumentPageDocumentFactory.create(page=self, **official_documents_page_document)
    #         return
