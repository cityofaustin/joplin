#!/usr/bin/env bash

echo "Running migrations: (${DEPLOYMENT_MODE}) ..."
python ./joplin/manage.py migrate --noinput

if [ "${DEPLOYMENT_MODE}" = "PRODUCTION" ] || [  "${DEPLOYMENT_MODE}" = "STAGING"  ]; then
    python ./joplin/manage.py collectstatic --noinput
else
    echo "Static files are only collected on STAGING or PRODUCTION, current environment: ${DEPLOYMENT_MODE}"
fi;
