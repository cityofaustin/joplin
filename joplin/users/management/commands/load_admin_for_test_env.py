from django.core.management.base import BaseCommand, CommandError
import users.fixtures as user_fixtures

'''
    Loads superadmin for API tests.

    Run with:
    pipenv run python joplin/manage.py load_admin_for_test_env
'''
class Command(BaseCommand):
    help = "Loads apitest@austintexas.io user"

    def handle(self, *args, **options):
        user_fixtures.admin_for_test_env()
