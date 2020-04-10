from pages.official_documents_page.models import OfficialDocumentPage
from wagtail.documents.models import Document
from pages.official_documents_page.factories import OfficialDocumentPageFactory, DocumentFactory
import hashlib
from django.core.files.base import ContentFile

# Skips creating fixture if Page with slug already exists
def create_fixture(page_data, fixture_name):
    try:
        page = OfficialDocumentPage.objects.get(slug=page_data['slug'])
    except OfficialDocumentPage.DoesNotExist:
        page = None
    if page:
        print(f"Skipping official documents page fixture: {fixture_name}")
        return page

    page = OfficialDocumentPageFactory.create(**page_data)
    print(f"Built official documents page fixture: {fixture_name}")
    return page


def create_fixture_document(file_content, file_name):
    # add a document
    file_hash = hashlib.sha1(file_content).hexdigest()
    # Check if a document with the same hash has already been imported
    try:
        document = Document.objects.get(file_hash=file_hash)
    except Document.DoesNotExist:
        document = None
    if document:
        print(f"Skipping document fixture: {file_name}")
        return document

    document = DocumentFactory.create(file=ContentFile(file_content, name=file_name), title=file_name)
    print(f"Built document fixture: {file_name}")
    return document
