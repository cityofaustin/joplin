import os
from io import StringIO
from django.core.management.base import BaseCommand, CommandError
from django.core.management import call_command
from django.core.exceptions import ObjectDoesNotExist
from base.models import DeploymentLog
from django.db import connection
from django.conf import settings


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
            if not load_data_result:
                LOAD_DATA = os.getenv("LOAD_DATA")
                DATABASE_URL = os.getenv("DATABASE_URL")
                if (LOAD_DATA == "prod"):
                    print("Adding prod datadump")
                    run_load_data_command('db/system-generated/prod.datadump.json')
                    DeploymentLog(operation="load_data", value="prod", completed=True).save()
                elif (LOAD_DATA == "staging"):
                    print("Adding staging datadump")
                    run_load_data_command('db/system-generated/staging.datadump.json')
                    DeploymentLog(operation="load_data", value="staging", completed=True).save()
                elif (LOAD_DATA == "dummy"):
                    print("Adding dummy datadump")
                    run_load_data_command('db/system-generated/dummy.datadump.json')
                    DeploymentLog(operation="load_data", value="dummy", completed=True).save()
                elif (LOAD_DATA == "new_datadump"):
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

            load_fixture(
                "load_test_admin",
                'db/fixtures/local_admin_user.json',
                (
                    os.getenv("DEPLOYMENT_MODE") == "LOCAL"
                    or settings.V3_WIP # if we don't LOAD_DATA in v3, we still need to add a test admin user
                )
            )
            # load_fixture(
            #     "load_janis_branch_settings",
            #     'db/fixtures/janis_branch_settings.json',
            #     (
            #         not os.getenv("DEPLOYMENT_MODE") in ("STAGING", "PRODUCTION")
            #         and not settings.V3_WIP
            #     )
            # )
            # load_fixture(
            #     "set_group_permissions",
            #     'db/fixtures/group_permissions_settings.json',
            #     (
            #         not os.getenv("DEPLOYMENT_MODE") in ("STAGING", "PRODUCTION")
            #         and not settings.V3_WIP
            #     )
            # )
            load_fixture(
                "set_themes",
                'db/fixtures/themes.json',
                (os.getenv("DEPLOYMENT_MODE") == "LOCAL")
            )

        finally:
            stdout.close()
            stderr.close()
