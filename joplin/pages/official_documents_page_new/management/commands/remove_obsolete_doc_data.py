from django.core.management.base import BaseCommand, CommandError
from pages.official_documents_page.models import OfficialDocumentPageDocument
from pages.official_documents_page.models import OfficialDocumentPage


def remove_obsolete_doc_data():
    OfficialDocumentPageDocument.objects.all().delete()
    OfficialDocumentPage.objects.all().delete()
    

class Command(BaseCommand):
    help = "Removes obsolete document data, after copy new official document pages has been run"

    def handle(self, *args, **options):
        remove_obsolete_doc_data()


