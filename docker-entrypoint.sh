#!/usr/bin/env bash
set -o errexit

# Docker Container Entry Point
# This script sets the command and parameters that will be executed first when a container is started.
# $DEPLOYMENT_MODE is set in app.Dockerfile at image build time

# Seed test data into Joplin from migration_test generated backup
function load_backup_data {
  echo "Adding backup data"
  python ./joplin/manage.py loaddata ./joplin/db/system-generated/seeding.datadump.json
}

# Add initial admin user to Database
function load_test_admin {
  echo "Adding test admin user for local development."
  python ./joplin/manage.py loaddata ./joplin/db/system-generated/local_admin_user.json
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
    if [ "$LOAD_PROD_DATA" == "on" ]; then
      # Option for migration_test.sh to source directly from production
      python ./joplin/manage.py loaddata ./joplin/db/system-generated/tmp_production.datadump.json
      sanitize_revision_data
      load_test_admin
    elif [ "$LOAD_DATA" == "on" ]; then
      load_backup_data
    else
      load_test_admin
    fi
  ;;
  REVIEW)
    load_backup_data
    # Let's try being reckless and doing that static thing here too.
    echo "Collecting static files"
    python ./joplin/manage.py collectstatic --noinput --verbosity 2;
  ;;
  STAGING|PRODUCTION)
    echo "Collecting static files"
    python ./joplin/manage.py collectstatic --noinput --verbosity 2;
  ;;
esac

exec "$@"
