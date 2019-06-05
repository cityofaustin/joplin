#!/usr/bin/env bash
set -o errexit

# Docker Container Entry Point
# This script sets the command and parameters that will be executed first when a container is started.
# $DEPLOYMENT_MODE is set in app.Dockerfile at image build time

function load_backup_data {
  echo "Adding backup data"
  python ./joplin/manage.py loaddata ./joplin/db/system-generated/*.datadump.json
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

# makes migrations, with merge flag to handle conflics
echo "making Schema Migrations"
python ./joplin/manage.py makemigrations --merge --noinput

# Run schema Migrations Only (Static files can remain local)
echo "Running schema Migrations"
python ./joplin/manage.py migrate --noinput

case "${DEPLOYMENT_MODE}" in
  LOCAL)
    # Allow option for data loading if DEPLOYMENT_MODE == "local"
    if [ "$LOAD_DATA" = "on" ]; then
      # Seed test data into Joplin
      load_backup_data
    else
      # Add initial admin user to Database if we aren't loading data
      echo "Adding test admin user for local development."
      python ./joplin/manage.py loaddata ./joplin/db/system-generated/local_admin_user.json
    fi
  ;;
  REVIEW)
    load_backup_data
    # Let's try being reckless and doing that static thing here too.
    echo "Collecting static files"
    python ./joplin/manage.py collectstatic --noinput;
  ;;
  STAGING|PRODUCTION)
    echo "Collecting static files"
    python ./joplin/manage.py collectstatic --noinput;
  ;;
esac

exec "$@"
