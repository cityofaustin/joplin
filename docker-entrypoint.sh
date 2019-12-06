#!/usr/bin/env bash
set -o errexit

# Docker Container Entry Point
# This script sets the command and parameters that will be executed first when a container is started.
# $DEPLOYMENT_MODE is set in app.Dockerfile at image build time

function sanitize_revision_data {
  echo "Sanitizing Revisions data"
  psql $DATABASE_URL -f ./scripts/sanitize_revision_data.sql
}

function set_group_permissions {
  echo "Setting editor and moderator group permissions"
  python ./joplin/manage.py loaddata ./joplin/db/fixtures/group_permissions_settings.json
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
  LOCAL|REVIEW)
    python ./joplin/manage.py load_joplin_data
  ;;
<<<<<<< HEAD
esac
case "${DEPLOYMENT_MODE}" in
  REVIEW|STAGING|PRODUCTION)
=======
  REVIEW)
    load_prod_datadump
    load_janis_branch_settings
    set_group_permissions
    echo "Collecting static files"
    python ./joplin/manage.py collectstatic --noinput;
  ;;
  STAGING|PRODUCTION)
>>>>>>> 3cb2a3eaba56db31145c4cdd864fa8d086703b84
    echo "Collecting static files"
    python ./joplin/manage.py collectstatic --noinput;
  ;;
esac

exec "$@"
