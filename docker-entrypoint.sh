#!/usr/bin/env bash
set -o errexit

#
# Docker Container Entry Point (Local)
# This script sets the command and parameters that will be executed first when a container is started.
#

# We are on a local instance, wait until the deployment is available for connections.
# Loop sleep every second until a connection is available.
until psql $DATABASE_URL -c '\q'; do
  >&2 echo "Postgres is unavailable - sleeping ..."
  sleep 1
done
>&2 echo "Postgres is up - executing command"

# if [ "$MIGRATION_TEST" = "on" ]; then
#   # Load backup data loaded in with $DATADUMP_LOCATION
#   echo "Adding migration_test_backup_data"
#   python ./joplin/manage.py loaddata ./app/joplin/db/data/migration_test_backup_data.json
# elif [ "$LOAD_DATA" = "on" ]; then
#   # Seed test data into Joplin
#   echo "Adding backup data"
#   python ./joplin/manage.py loaddata ./joplin/db/data/main_datadump.json
# fi

# Run Data Migrations Only (Static files can remain local)
echo "Running Data Migrations"
python ./joplin/manage.py migrate --noinput

if [ "$MIGRATION_TEST" = "on" ]; then
  # Load Data for Migration Tests
  LOAD_DATA="on"
fi

if [ "$LOAD_DATA" = "on" ]; then
  # Seed test data into Joplin
  echo "Adding backup data"
  python ./joplin/manage.py loaddata ./joplin/db/data/main_datadump.json
else
  # Add initial admin user to Database if we aren't loading data
  echo "Adding test admin user for local development."
  python ./joplin/manage.py loaddata ./joplin/db/data/local_admin_user.json
fi

exec "$@"
