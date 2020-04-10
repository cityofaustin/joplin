from django.core.management.base import BaseCommand, CommandError
import pages.official_documents_page.fixtures as official_documents_page_fixtures

'''
    Loads topic page fixtures into your joplin environment.

    Run with:
    pipenv run python joplin/manage.py load_test_official_documents_pages
'''
class Command(BaseCommand):
    help = "Loads test data for manual exploration of test topic pages"

    def handle(self, *args, **options):
        official_documents_page_fixtures.load_all()
