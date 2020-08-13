from urllib3.request import RequestMethods
from django.core.management.base import BaseCommand, CommandError
from pages.official_documents_page.models import OfficialDocumentPage


def extract_document_text():
    """
    """

    all_document_pages = OfficialDocumentPage.objects.all()

    url_base = 'https://joplin3-austin-gov-static.s3.amazonaws.com/production'

    for page in all_document_pages:
        '''
        get the document url
        get the data from the document url
        
        '''
        doc_url = url_base + page.document.url
        print(page)


class Command(BaseCommand):
    help = ""

    def handle(self, *args, **options):
        extract_document_text()
