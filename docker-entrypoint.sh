#!/usr/bin/env bash
set -o errexit

# Docker Container Entry Point
# This script sets the command and parameters that will be executed first when a container is started.
# $ENV is set in Dockerfile.app at image build time

if [ $ENV == "local" ]; then
  # We are on a local instance, wait until the deployment is available for connections.
  # Loop sleep every second until a connection is available.
  until psql $DATABASE_URL -c '\q'; do
    >&2 echo "Postgres is unavailable - sleeping ..."
    sleep 1
  done
  >&2 echo "Postgres is up - executing command"
fi

# Run Data Migrations Only (Static files can remain local)
echo "Running Data Migrations"
python ./joplin/manage.py migrate --noinput

if [ $ENV == "local" ]; then
  # Allow option for data loading if ENV == "local"
  if [ "$LOAD_DATA" = "on" ]; then
    # Seed test data into Joplin
    echo "Adding backup data"
    python ./joplin/manage.py loaddata ./joplin/db/data/migration_datadump_*.json
  else
    # Add initial admin user to Database if we aren't loading data
    echo "Adding test admin user for local development."
    python ./joplin/manage.py loaddata ./joplin/db/data/local_admin_user.json
  fi
else
  # If not on "local", don't load data
  echo "-- Entrypoint Executed (docker-entrypoint.sh)"
  echo "--    APPLICATION_NAME:   ${APPLICATION_NAME}"
  echo "--    Bucket:             ${AWS_S3_BUCKET}"
  echo "--    Bucket User:        ${AWS_S3_USER}"
  echo "--    Bucket ID:          ${AWS_S3_KEYID}"
fi

exec "$@"
