from django.core.management.base import BaseCommand, CommandError
from pages.service_page.fixtures.with_steps import load_with_steps

# pipenv run python joplin/manage.py load_test_service_pages
class Command(BaseCommand):
    help = "Loads test data for manual exploration of test service_pages"

    def handle(self, *args, **options):
        load_with_steps()
