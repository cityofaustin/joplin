from django.core.management.base import BaseCommand, CommandError
import base.fixtures.administrative.mandatory_fixtures as mandatory_fixtures

'''
    Loads fixtures that are required for Joplin to run properly.

    Run with:
    pipenv run python joplin/manage.py load_mandatory_fixtures
'''
class Command(BaseCommand):
    help = "Loads test data for manual exploration of test service_pages"

    def handle(self, *args, **options):
        mandatory_fixtures.load_all()
