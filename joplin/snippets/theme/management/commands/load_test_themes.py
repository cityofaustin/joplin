from django.core.management.base import BaseCommand, CommandError
import snippets.theme.fixtures as theme_fixtures

'''
    Loads theme fixtures into your joplin environment.

    Run with:
    pipenv run python joplin/manage.py load_test_themes
'''
class Command(BaseCommand):
    help = "Loads test data for manual exploration of test themes"

    def handle(self, *args, **options):
        theme_fixtures.load_all()
