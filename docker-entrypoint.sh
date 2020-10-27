#!/usr/bin/env bash
set -o errexit

# Docker Container Entry Point
# This script sets the command and parameters that will be executed first when a container is started.
# $DEPLOYMENT_MODE is set in app.Dockerfile at image build time

case "${DEPLOYMENT_MODE}" in
  LOCAL|TEST)
    # We are on a local instance, wait until the deployment is available for connections.
    # Loop sleep every second until a connection is available.
    until psql $DATABASE_URL -c '\q'; do
      >&2 echo "Postgres is unavailable - sleeping ..."
      sleep 1
    done
    >&2 echo "Postgres is up - executing command"
  ;;
esac

# Run schema Migrations Only (Static files can remain local)
echo "Running schema Migrations"
python ./joplin/manage.py migrate --noinput
# Load mandatory initial data required for any instance
python joplin/manage.py load_mandatory_fixtures

case "${DEPLOYMENT_MODE}" in
  LOCAL|REVIEW|TEST)
    python ./joplin/manage.py load_joplin_data
  ;;
esac

# Update our search index in case newly loaded data or existing data has not been indexed yet.
python ./joplin/manage.py update_index

case "${DEPLOYMENT_MODE}" in
  REVIEW|STAGING|PRODUCTION)
    echo "Collecting static files"
    python ./joplin/manage.py collectstatic --noinput;
  ;;
esac

exec "$@"
