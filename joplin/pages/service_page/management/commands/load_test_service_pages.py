from django.core.management.base import BaseCommand, CommandError
import pages.service_page.fixtures as service_page_fixtures

'''
    Loads service_page fixtures into your joplin environment.

    Run with:
    pipenv run python joplin/manage.py load_test_service_pages
'''
class Command(BaseCommand):
    help = "Loads test data for manual exploration of test service_pages"

    def handle(self, *args, **options):
        service_page_fixtures.step_with_1_location()
