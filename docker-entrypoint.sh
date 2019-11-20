#!/usr/bin/env bash
set -o errexit

# Docker Container Entry Point
# This script sets the command and parameters that will be executed first when a container is started.
# $DEPLOYMENT_MODE is set in app.Dockerfile at image build time

# Seed prior prod datadump into Joplin from migration_test generated backup
function load_prod_datadump {
  echo "Adding prod datadump"
  python ./joplin/manage.py loaddata ./joplin/db/system-generated/prod.datadump.json
}

# Seed prior staging datadump into Joplin from migration_test generated backup
function load_staging_datadump {
  echo "Adding staging datadump"
  python ./joplin/manage.py loaddata ./joplin/db/system-generated/staging.datadump.json
}

# Add initial configs to handle Publishing and Previewing on PR Apps
function load_janis_branch_settings {
  echo "Adding Janis Branch settings"
  python ./joplin/manage.py loaddata ./joplin/db/fixtures/janis_branch_settings.json
}

# Add initial admin user to Database
function load_test_admin {
  echo "Adding test admin user for local development."
  python ./joplin/manage.py loaddata ./joplin/db/fixtures/local_admin_user.json
}

function sanitize_revision_data {
  echo "Sanitizing Revisions data"
  psql $DATABASE_URL -f ./scripts/sanitize_revision_data.sql
}

if [ $DEPLOYMENT_MODE == "LOCAL" ]; then
  # We are on a local instance, wait until the deployment is available for connections.
  # Loop sleep every second until a connection is available.
  until psql $DATABASE_URL -c '\q'; do
    >&2 echo "Postgres is unavailable - sleeping ..."
    sleep 1
  done
  >&2 echo "Postgres is up - executing command"
fi

# Run schema Migrations Only (Static files can remain local)
echo "Running schema Migrations"
python ./joplin/manage.py migrate --noinput

case "${DEPLOYMENT_MODE}" in
  LOCAL)
    if [ "$LOAD_NEW_DATADUMP" == "on" ]; then
      # Option for migration_test.sh to source directly from a new production or staging datadump
      python ./joplin/manage.py loaddata ./joplin/db/system-generated/tmp.datadump.json
      sanitize_revision_data
      load_test_admin
    elif [ "$LOAD_DATA" == "on" ] || [ "$LOAD_PROD_DATA" == "on" ]; then
      load_prod_datadump
    elif [ "$LOAD_STAGING_DATA" == "on" ]; then
      load_staging_datadump
    else
      load_test_admin
    fi
    load_janis_branch_settings
  ;;
  REVIEW)
    load_prod_datadump
    load_janis_branch_settings
    echo "Collecting static files"
    python ./joplin/manage.py collectstatic --noinput;
  ;;
  STAGING|PRODUCTION)
    echo "Collecting static files"
    python ./joplin/manage.py collectstatic --noinput;
  ;;
esac

exec "$@"
