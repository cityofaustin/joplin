#!/usr/bin/env bash

echo "Running migrations..."
python ./joplin/manage.py migrate --noinput

if [ "$DEPLOYMENT_MODE" = "PRODUCTION" ];
then
    python ./joplin/manage.py collectstatic --noinput
else
    echo "Static files will not be collected (migrated) to S3"
fi;
