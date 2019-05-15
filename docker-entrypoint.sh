#!/usr/bin/env bash
set -o errexit

#
# Docker Container Entry Point (Local)
# This script sets the command and parameters that will be executed first when a container is started.
#

function load_latest_migration_datadump {
  echo "Adding backup data"
  python ./joplin/manage.py loaddata ./joplin/db/fixtures/migration_datadump_*.json
}

# We are on a local instance, wait until the deployment is available for connections.
# Loop sleep every second until a connection is available.
until psql $DATABASE_URL -c '\q'; do
  >&2 echo "Postgres is unavailable - sleeping ..."
  sleep 1
done
>&2 echo "Postgres is up - executing command"

# Run Data Migrations Only (Static files can remain local)
echo "Running Data Migrations"
python ./joplin/manage.py migrate --noinput

if [ "$LOAD_DATA" = "on" ]; then
  # Seed test data into Joplin
  load_latest_migration_datadump
else
  # Add initial admin user to Database if we aren't loading data
  echo "Adding test admin user for local development."
  python ./joplin/manage.py loaddata ./joplin/db/data/local_admin_user.json
fi

exec "$@"
