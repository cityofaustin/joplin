#!/usr/bin/env bash
set -o errexit

# Docker Container Entry Point
# This script sets the command and parameters that will be executed first when a container is started.
# $DEPLOYMENT_MODE is set in app.Dockerfile at image build time

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
  LOCAL|REVIEW)
    python ./joplin/manage.py load_joplin_data
  ;;
esac
case "${DEPLOYMENT_MODE}" in
  REVIEW|STAGING|PRODUCTION)
    echo "Collecting static files"
    python ./joplin/manage.py collectstatic --noinput;
  ;;
esac

exec "$@"
