from wagtail.documents.models import Document
from pages.official_documents_page.factories import DocumentFactory
import hashlib
from django.core.files.base import ContentFile


from pages.base_page.fixtures.helpers.create_fixture_map import create_fixture_map
create_fixture = create_fixture_map["official_document"]


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
