from django.core.management.base import BaseCommand, CommandError
from django.utils.text import slugify
from pages.official_documents_page_new.fixtures.helpers.create_fixture import create_fixture as create_document_fixture
from groups.models import Department
from pages.official_documents_page.models import OfficialDocumentPageDocument
from pages.official_documents_collection.models import OfficialDocumentCollection
from pages.home_page.models import HomePage


def copy_official_document_page_documents():
    """

    :return:
    """

    home = HomePage.objects.first()
    all_document_page_documents = OfficialDocumentPageDocument.objects.all()

    for page in all_document_page_documents:
        parent_page = OfficialDocumentCollection.objects.get(slug=page.slug+'-copy')
        page_data = {
            "imported_revision_id": None,
            "live": True,
            "published": True, # check with nick about this
            "parent": home,
            "coa_global": False,
            "title": page.title,
            "title_es": page.title_es,
            "slug": slugify(page.title, allow_unicode=True),
            "add_departments": {
                "departments": [Department.objects.get(name='Office of Police Oversight')], # hard coding this
            },
            "summary": page.summary,
            "summary_es": page.summary_es,
            "name": page.name,
            "name_es": page.name_es,
            "authoring_office": page.authoring_office,
            "authoring_office_es": page.authoring_office_es,
            "date": page.date,
            "document": page.document,
            "document_es": page.document_es,
            "add_official_document_collection": {
                "official_document_collection": [parent_page],
            },
            "owner": parent_page.owner,
        }
        print('******  ', page_data)
        create_document_fixture(page_data, 'new official document page')


class Command(BaseCommand):
    help = "Copies data from OfficialDocumentPageDocuments to Official Document Pages New Model"

    def handle(self, *args, **options):
        copy_official_document_page_documents()



