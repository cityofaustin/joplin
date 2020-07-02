import json
from django.core.management.base import BaseCommand, CommandError
from pages.official_documents_collection.fixtures.helpers.create_fixture import create_fixture
from pages.official_documents_page.models import OfficialDocumentPage
from pages.home_page.models import HomePage
from pages.topic_page.models import TopicPage


def copy_official_page_data():
    """
    Official document pages have been split out into Official Document Collections and Official Document Pages
    This function copies the information
    """
    home = HomePage.objects.first()
    all_official_document_pages = OfficialDocumentPage.objects.all()

    for page in all_official_document_pages.iterator():
        old_page_data = json.loads(page.to_json())
        print(old_page_data)
        topics = []
        for t in old_page_data['topics']:
            topics.append(TopicPage.objects.get(id=t['topic']))

        page_data = {
            "imported_revision_id": None,
            "live": True,
            "published": old_page_data['published'],
            "parent": home,
            "coa_global": False,
            "title": old_page_data['title'],
            "slug": old_page_data['slug'] + '-copy',
            "add_topics": {
                 "topics": topics,
            },
            "description": old_page_data['description'],
            "description_es": old_page_data['description_es'],
        }

        print('******* ', page_data)
        create_fixture(page_data, 'official collection copy')


class Command(BaseCommand):
    help = "Loads test data for manual exploration of test topic pages"

    def handle(self, *args, **options):
        copy_official_page_data()



