from django.core.management.base import BaseCommand, CommandError
import pages.event_page.fixtures as event_page_fixtures

'''
    Loads event_page fixtures into your joplin environment.

    Run with:
    pipenv run python joplin/manage.py load_test_event_pages
'''
class Command(BaseCommand):
    help = "Loads test data for manual exploration of test event_pages"

    def handle(self, *args, **options):
        event_page_fixtures.load_all()
