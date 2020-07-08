import factory
from pages.official_documents_page.models import OfficialDocumentPage, OfficialDocumentCollectionDocument
from pages.topic_page.factories import JanisBasePageWithTopicsFactory
from pages.official_documents_collection.factories import OfficialDocumentCollectionFactory
from wagtail.documents.models import Document


class DocumentFactory(factory.DjangoModelFactory):
    @classmethod
    def create(cls, *args, **kwargs):
        return super(DocumentFactory, cls).create(*args, **kwargs)

    class Meta:
        model = Document


class OfficialDocumentCollectionDocumentFactory(factory.django.DjangoModelFactory):
    page = factory.SubFactory(
        'base_page.factories.JanisBasePageWithTopicsFactory',
        add_departments__dummy=False,
    )
    official_document_collection = factory.SubFactory(
        OfficialDocumentCollectionFactory,
        add_departments__dummy=False,
    )

    class Meta:
        model = OfficialDocumentCollectionDocument


class OfficialDocumentPageFactory(JanisBasePageWithTopicsFactory):
    class Meta:
        model = OfficialDocumentPage

    # document = factory.SubFactory(
    #     DocumentFactory
    # )

    @factory.post_generation
    def add_official_document_collection(self, create, extracted, **kwargs):
        if extracted:
            # A list of official document collections were passed in, use them
            for collection in extracted['official_document_collection']:
                OfficialDocumentCollectionDocumentFactory.create(page=self, official_document_collection=collection)
            return

        # pass "add_topics__dummy"=True into Factory() to make dummy document collections
        if create:
            if kwargs.get("dummy", False):
                OfficialDocumentCollectionFactory.create_batch(2, page=self)



# import factory
# from pages.official_documents_page.models import OfficialDocumentPageOld, OfficialDocumentPageDocument
# from pages.topic_page.factories import JanisBasePageWithTopicsFactory
# from wagtail.documents.models import Document
#
#
# class OfficialDocumentPageFactory(JanisBasePageWithTopicsFactory):
#     class Meta:
#         model = OfficialDocumentPageOld
#
#     @factory.post_generation
#     def add_official_documents_page_documents(self, create, extracted, **kwargs):
#         if extracted:
#             # A list of documents were passed in, use them
#             # reversed() to preserve insert order.
#             for official_documents_page_document in reversed(extracted['official_documents_page_documents']):
#                 OfficialDocumentPageDocumentFactory.create(page=self, **official_documents_page_document)
#             return
#
#
# class DocumentFactory(factory.DjangoModelFactory):
#     @classmethod
#     def create(cls, *args, **kwargs):
#         return super(DocumentFactory, cls).create(*args, **kwargs)
#
#     class Meta:
#         model = Document
#
#
# class OfficialDocumentPageDocumentFactory(factory.DjangoModelFactory):
#     page = factory.SubFactory(
#         'official_documents_page.factories.OfficialDocumentsPageFactory',
#     )
#
#     document = factory.SubFactory(
#         DocumentFactory
#     )
#
#     class Meta:
#         model = OfficialDocumentPageDocument
