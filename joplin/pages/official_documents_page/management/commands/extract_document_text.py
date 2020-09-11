import urllib3
import io
import fitz
from django.core.management.base import BaseCommand, CommandError
from pages.official_documents_page.models import OfficialDocumentPage


def extract_text_from_url(url):
    """
    :param url: string, address of pdf
    :return: string with contents extracted from pdf located at url
    """
    http = urllib3.PoolManager()
    resp = http.request('GET', url)
    file_stream = io.BytesIO(resp.data)
    text = ''
    pdf_doc = fitz.open(stream=file_stream, filetype='pdf')
    for page in pdf_doc:
        text += page.getText()
    return text


def extract_document_text():
    """
    Iterates through Official Document Pages
    if body is empty, retrieve document at url and save text in the body
    """
    all_document_pages = OfficialDocumentPage.objects.all()
    print(f'Beginning extraction...')

    for page in all_document_pages:
        print(f'Page id {page.id}')
        # Check if page body already has content, if so skip
        if len(page.body) > 0:
            continue
        if page.document and page.document.url:
            filename = page.document.url.split('docs')[1]
            print(f'reading {filename}')
            extracted_text = extract_text_from_url(page.document.url)
            page.body = extracted_text
            page.save()
        else:
            print(f'Official Document Page with id {page.id} does not have a document')


class Command(BaseCommand):
    help = "Script to extract text from pdfs on OfficialDocumentPages and save in body"

    def handle(self, *args, **options):
        extract_document_text()
