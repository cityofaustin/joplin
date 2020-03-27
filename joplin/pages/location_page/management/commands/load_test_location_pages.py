from django.core.management.base import BaseCommand, CommandError
import pages.location_page.fixtures as location_page_fixtures

'''
    Loads service_page fixtures into your joplin environment.

    Run with:
    pipenv run python joplin/manage.py load_test_location_pages
'''
class Command(BaseCommand):
    help = "Loads test data for manual exploration of test location_pages"

    def handle(self, *args, **options):
        location_page_fixtures.load_all()
