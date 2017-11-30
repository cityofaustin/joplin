#!/usr/bin/env bash

set -o errexit

CONTAINER_NAME="joplin"
echo "Configuring container $CONTAINER_NAME..."

echo $'\nCreating DB schema'
docker exec "$CONTAINER_NAME" ./joplin/manage.py migrate

echo $'\nLoading initial data'
docker exec "$CONTAINER_NAME" ./joplin/manage.py loaddata fixtures/initial.json
