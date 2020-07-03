import json
from django.core.management.base import BaseCommand, CommandError
from django.db.utils import ProgrammingError
from pages.official_documents_collection.fixtures.helpers.create_fixture import create_fixture as create_collection_fixture
from pages.official_documents_page.models import OfficialDocumentPage
from pages.home_page.models import HomePage
from pages.topic_page.models import TopicPage


def copy_official_page_data():
    """
    Official document pages have been split out into Official Document Collections and Official Document Pages
    This function copies the information, creating OfficialDocumentCollections with the same information as
    Official Document Pages except the list of documents, which will be copied in <insert func name>
    """
    home = HomePage.objects.first()
    all_official_document_pages = OfficialDocumentPage.objects.all()

    for page in all_official_document_pages.iterator():
        old_page_data = json.loads(page.to_json())
        topics = []
        for t in old_page_data['topics']:
            topics.append(TopicPage.objects.get(id=t['topic']))
        # the departments the factory wants aren't DepartmentPages, but rather the Department model itself.
        # page.departments returns a list of Department pages
        departments = []
        for d in page.departments():
            departments.append(d.department)

        page_data = {
            "imported_revision_id": None,
            "live": old_page_data['live'],
            "published": old_page_data['published'],
            "parent": home,
            "coa_global": old_page_data['coa_global'],
            "title": old_page_data['title'],
            "slug": old_page_data['slug'] + '-copy',
            "add_departments": {
                "departments": departments,
            },
            "add_topics": {
                 "topics": topics,
            },
            "description": old_page_data['description'],
            "description_es": old_page_data['description_es'],
            "owner": page.owner,
        }

        create_collection_fixture(page_data, 'official collection copy')


class Command(BaseCommand):
    help = "Copies data from Official Document Pages to Official Document Collections "

    def handle(self, *args, **options):
        try:
            copy_official_page_data()
        except ProgrammingError:
            raise CommandError('Error. Check to see that all migrations have been run.')


