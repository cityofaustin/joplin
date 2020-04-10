from django.core.management.base import BaseCommand, CommandError
import pages.department_page.fixtures as department_page_fixtures

'''
    Loads department_page fixtures into your joplin environment.

    Run with:
    pipenv run python joplin/manage.py load_test_department_pages
'''
class Command(BaseCommand):
    help = "Loads test data for manual exploration of test department_pages"

    def handle(self, *args, **options):
        department_page_fixtures.load_all()
