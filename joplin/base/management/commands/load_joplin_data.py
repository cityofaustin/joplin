import os
from io import StringIO
from django.core.management.base import BaseCommand, CommandError
from django.core.management import call_command
from django.core.exceptions import ObjectDoesNotExist
from base.models import DeploymentLog
from django.db import connection
from django.conf import settings

import snippets.contact.fixtures as contact_fixtures
import snippets.theme.fixtures as theme_fixtures
import pages.topic_collection_page.fixtures as topic_collection_page_fixtures
import pages.topic_page.fixtures as topic_page_fixtures
import pages.service_page.fixtures as service_page_fixtures
import pages.official_documents_page.fixtures as official_documents_page_fixtures
import pages.location_page.fixtures as location_page_fixtures
import pages.event_page.fixtures as event_page_fixtures
import pages.department_page.fixtures as department_page_fixtures
import pages.news_page.fixtures as news_page_fixtures
import users.fixtures as user_fixtures
from importer.import_everything import import_everything


class Command(BaseCommand):
    help = "Load initial seeding data into your app"

    def handle(self, *args, **options):
        stdout = StringIO()
        stderr = StringIO()

        def run_load_data_command(file):
            filepath = os.path.join(settings.BASE_DIR, 'joplin', file)
            call_command('loaddata', filepath, stdout=stdout, stderr=stderr)
            if stdout.getvalue():
                print(stdout.getvalue())
                stdout.truncate(0)
            if stderr.getvalue():
                print(stderr.getvalue())
                stderr.truncate(0)
                raise

        # Loads fixture data if it hasn't been loaded already
        # operation_name: name of the operation for the DeploymentLog
        # fixture_name: name of the fixture_name that the operation loads
        # condition: condition required for this operation to be run
        def load_fixture(operation_name, fixture_name, condition):
            try:
                info = DeploymentLog.objects.get(operation=operation_name)
                result = info.completed
                if result:
                    print(f"Skipping previously loaded fixture {fixture_name}")
            except ObjectDoesNotExist:
                result = None
            if (
                not result and condition
            ):
                print(f"Adding fixture {fixture_name}")
                run_load_data_command(fixture_name)
                DeploymentLog(operation=operation_name, completed=True).save()

        try:
            # Load seeding data if data hasn't been loaded already
            try:
                info = DeploymentLog.objects.get(operation="load_data")
                load_data_result = info.completed
                if load_data_result:
                    print(f"Already loaded data from {info.value}")
            except ObjectDoesNotExist:
                load_data_result = None
            LOAD_DATA = os.getenv("LOAD_DATA")
            # Allow re-running of 'fixtures' data
            if LOAD_DATA == 'fixtures' or LOAD_DATA == 'test':
                print("Adding fixture data")
                contact_fixtures.load_all()
                theme_fixtures.load_all()
                topic_collection_page_fixtures.load_all()
                topic_page_fixtures.load_all()
                service_page_fixtures.load_all()
                # official_documents_page_fixtures.load_all()
                event_page_fixtures.load_all()
                location_page_fixtures.load_all()
                department_page_fixtures.load_all()
                news_page_fixtures.load_all()

                # TODO: incorporate logging into DeploymentLog?
            if LOAD_DATA == 'importer':
                print("Importing data from http://joplin-staging.herokuapp.com/api/graphql")
                import_everything()
            elif not load_data_result:
                if LOAD_DATA == 'prod':
                    print("Adding prod datadump")
                    run_load_data_command('db/system-generated/prod.datadump.json')
                    DeploymentLog(operation="load_data", value="prod", completed=True).save()
                elif LOAD_DATA == "new_datadump":
                    print("Adding new migration test datadump")
                    run_load_data_command('db/system-generated/tmp.datadump.json')

                    # Runs code from /db/scripts/sanitize_revision_data.sql
                    print("Sanitizing Revisions data")
                    sanitize_revision_path = os.path.join(settings.BASE_DIR, 'joplin/db/scripts/sanitize_revision_data.sql')
                    sanitize_revision_file = open(sanitize_revision_path, 'r')
                    sanitize_revision_sql = sanitize_revision_file.read()
                    sanitize_revision_file.close()
                    with connection.cursor() as cursor:
                        # The cursor will handle error throwing if there are any bugs in your sql code.
                        cursor.execute(sanitize_revision_sql)
                        print(cursor.statusmessage)
                else:
                    print("Not adding any datadumps\n")

            if settings.IS_LOCAL or settings.IS_REVIEW:
                user_fixtures.superadmin()

            # Add pytest superadmin
            if LOAD_DATA == 'test':
                user_fixtures.admin_for_test_env()

        finally:
            stdout.close()
            stderr.close()
