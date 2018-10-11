#!/usr/bin/env bash
set -o errexit

#
# Docker Container Entry Point (Local)
# This script sets the command and parameters that will be executed first when a container is started.
#

if [ "$DEPLOYMENT_MODE" = "LOCAL" ]; then
    # We are on a local instance, wait until the deployment is available for connections.
    # Loop sleep every second until a connection is available.
    until psql $DATABASE_URL -c '\q'; do
      >&2 echo "Postgres is unavailable - sleeping ..."
      sleep 1
    done

    >&2 echo "Postgres is up - executing command"

else
    # We are on a production or staging instance (on the cloud), start any time.
    echo "Running on production, start migration immediately."
fi

# Run Data Migrations Only (Static files can remain local)
python ./joplin/manage.py migrate --noinput

# DB Restore if load data is
if [ "$LOAD_DATA" == "on" ]; then
    echo "Loading data from backup."
    python ./joplin/manage.py dbrestore --noinput
fi


exec "$@"


