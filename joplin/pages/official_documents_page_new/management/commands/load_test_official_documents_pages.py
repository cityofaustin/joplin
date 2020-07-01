from django.core.management.base import BaseCommand
import pages.official_documents_page_new.fixtures as official_documents_page_new_fixtures

'''
    Loads official document page fixtures into your joplin environment.

    Run with:
    pipenv run python joplin/manage.py load_test_topic_pages
'''
class Command(BaseCommand):
    help = "Loads test data for manual exploration of test document pages"

    def handle(self, *args, **options):
        official_documents_page_new_fixtures.load_all()
