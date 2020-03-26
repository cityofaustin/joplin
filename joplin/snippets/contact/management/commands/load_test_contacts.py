from django.core.management.base import BaseCommand, CommandError
import snippets.contact.fixtures as contact_fixtures

'''
    Loads service_page fixtures into your joplin environment.

    Run with:
    pipenv run python joplin/manage.py load_test_contacts
'''
class Command(BaseCommand):
    help = "Loads test data for manual exploration of test contacts"

    def handle(self, *args, **options):
        contact_fixtures.load_all()
