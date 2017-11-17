#!/usr/bin/env bash

set -o errexit

CONTAINER_NAME="joplin"
echo "Configuring container $CONTAINER_NAME..."

echo $'\nCreating DB schema'
docker exec "$CONTAINER_NAME" ./joplin/manage.py migrate

echo $'\nCreate a password for the "admin" superuser'
docker exec --interactive --tty "$CONTAINER_NAME" ./joplin/manage.py createsuperuser --username admin --email you@atx.gov
