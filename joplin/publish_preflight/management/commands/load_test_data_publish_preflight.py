from django.core.management.base import BaseCommand, CommandError
from publish_preflight.tests.utils.load_test_data import load_test_data

# pipenv run python joplin/manage.py load_test_data_publish_preflight
class Command(BaseCommand):
    help = "Loads test data for manual exploration of publish_preflight test data"

    def handle(self, *args, **options):
        load_test_data()
