from django.core.management.base import BaseCommand, CommandError
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
        page_data = {
            "imported_revision_id": None,
            "live": True,
            "published": True, # check with nick about this
            "parent": home,
            "coa_global": False,
            "title": page.title,
            "title_es": page.title_es,
            # "slug": old_page_data['slug'] + '-copy', what is the slug going to be
            "add_departments": {
                "departments": [Department.objects.get(name='Office of Police Oversight')], # OPO
            },
            "description": page.description,
            "description_es": page.description_es,
            "authoring_office": page.authoring_office,
            "authoring_office_es": page.authoring_office_es,
            "date": page.date,
            "add_official_document_collection": {
                "official_document_collection": OfficialDocumentCollection.objects.get(slug=page.page.slug+'-copy'),
            },
        }
        create_document_fixture(page_data, 'new official document page')


class Command(BaseCommand):
    help = "Copies data from OfficialDocumentPageDocuments to Official Document Pages New Model"

    def handle(self, *args, **options):
        copy_official_document_page_documents()



