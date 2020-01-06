import os, subprocess
from io import StringIO
from django.core.management.base import BaseCommand, CommandError
from django.core.management import call_command
from django.core.exceptions import ObjectDoesNotExist
from base.models import DeploymentLog

class Command(BaseCommand):
    help = "Load initial seeding data into your app"

    def handle(self, *args, **options):
        stdout = StringIO()
        stderr = StringIO()

        def run_load_data_command(filepath):
            call_command('loaddata', filepath, stdout=stdout, stderr=stderr)
            if stdout.getvalue():
                print(stdout.getvalue())
                stdout.truncate(0)
            if stderr.getvalue():
                print(stderr.getvalue())
                stderr.truncate(0)
                raise

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
                LOAD_DATA=os.getenv("LOAD_DATA")
                if (LOAD_DATA == "prod"):
                    print("Adding prod datadump")
                    run_load_data_command('./joplin/db/system-generated/prod.datadump.json')
                    DeploymentLog(operation="load_data",value="prod",completed=True).save()
                elif (LOAD_DATA == "staging"):
                    print("Adding staging datadump")
                    run_load_data_command('./joplin/db/system-generated/staging.datadump.json')
                    DeploymentLog(operation="load_data",value="staging",completed=True).save()
                elif (LOAD_DATA == "dummy"):
                    print("Adding dummy datadump")
                    run_load_data_command('./joplin/db/system-generated/dummy.datadump.json')
                    DeploymentLog(operation="load_data",value="dummmy",completed=True).save()
                elif (LOAD_DATA == "new_datadump"):
                    print("Adding new migration test datadump")
                    run_load_data_command('./joplin/db/system-generated/tmp.datadump.json')
                    print("Sanitizing Revisions data")
                    output = subprocess.run(re.split("\s+", f"psql ${DATABASE_URL} -f ./db/scripts/sanitize_revision_data.sql"),
                        capture_output=True,
                        text=True,
                    )
                    if output.stdout:
                        print(output.stdout)
                    if out.stderr:
                        print(output.stderr)
                        raise
                else:
                    print("Not adding any datadumps\n")

            # Load test admin user if it hasn't been loaded already
            try:
                info = DeploymentLog.objects.get(operation="load_test_admin")
                load_test_admin_result = info.completed
                if load_test_admin_result:
                    print("Already loaded test_admin")
            except ObjectDoesNotExist:
                load_test_admin_result = None
            if (
                not load_test_admin_result and
                (os.getenv("DEPLOYMENT_MODE") == "LOCAL")
            ):
                print("Adding test admin user for development.")
                run_load_data_command('./joplin/db/fixtures/local_admin_user.json')
                DeploymentLog(operation="load_test_admin",completed=True).save()

            # Load janis_branch_settings if they haven't been loaded already
            try:
                info = DeploymentLog.objects.get(operation="load_janis_branch_settings")
                load_janis_branch_settings_result = info.completed
                if load_janis_branch_settings_result:
                    print("Already loaded janis_branch_settings")
            except ObjectDoesNotExist:
                load_janis_branch_settings_result = None
            if (
                not load_janis_branch_settings_result and
                not os.getenv("DEPLOYMENT_MODE") in ("STAGING", "PRODUCTION")
            ):
                print("Adding Janis Branch settings")
                run_load_data_command('./joplin/db/fixtures/janis_branch_settings.json')
                DeploymentLog(operation="load_janis_branch_settings",completed=True).save()

            # Set group_permissions if they haven't been loaded already
            try:
                info = DeploymentLog.objects.get(operation="set_group_permissions")
                set_group_permissions_result = info.completed
                if set_group_permissions_result:
                    print("Already set group_permissions")
            except ObjectDoesNotExist:
                set_group_permissions_result = None
            if (
                not set_group_permissions_result and
                not os.getenv("DEPLOYMENT_MODE") in ("STAGING", "PRODUCTION")
            ):
                print("Setting editor and moderator group permissions")
                run_load_data_command('./joplin/db/fixtures/group_permissions_settings.json')
                DeploymentLog(operation="set_group_permissions",completed=True).save()
        finally:
            stdout.close()
            stderr.close()
