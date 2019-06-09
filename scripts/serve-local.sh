#!/usr/bin/env bash

set -o errexit

CURRENT_DIR=`dirname $BASH_SOURCE`
source $CURRENT_DIR/docker-helpers.sh

# Allows us to use BUILDKIT features like adding a --target to docker build
# Only works for "docker build" not "docker-compose ... --build"
export DOCKER_BUILDKIT=1

# Env Vars for use within Joplin
export JOPLIN_DB_HOST_PORT=5433
export JOPLIN_DB_CONTAINER_PORT=5432
export JOPLIN_APP_HOST_PORT=8000
export JOPLIN_APP_CONTAINER_PORT=80
export JANIS_URL=http://localhost:3000
export DATABASE_URL="postgres://joplin@db:${JOPLIN_DB_CONTAINER_PORT}/joplin"

# Build Args for use during build process
export COMPOSE_PROJECT_NAME=joplin
export DOCKER_TAG_APP="joplin-app:local"
export DOCKER_TAG_ASSETS="joplin-assets:local"
export DOCKER_TARGET_APP=joplin-local

# Stop any existing joplin containers that might still be running
echo "Stopping any $COMPOSE_PROJECT_NAME containers that might still be running"
stop_project_containers $COMPOSE_PROJECT_NAME

# Aside from the database dropping step, RELOAD_DATA does the same thing as LOAD_DATA
if [ "$RELOAD_DATA" == "on" ]; then
  export LOAD_DATA="on"
fi

# Delete old database containers for HARD_REBUILDs or RELOADs
if [ "$HARD_REBUILD" == "on" ] || [ "$RELOAD_DATA" == "on" ] || [ "$DROP_DB" == "on" ]; then
  echo "Deleting old joplin_db containes"
  docker ps -aq -f name=joplin_db_1 | while read CONTAINER ; do docker rm -f $CONTAINER ; done
fi

if [ "$HARD_REBUILD" == "on" ]; then
  echo 'HARD_REBUILD="on": Rebuilding containers without cache'
  echo "Rebuilding ${DOCKER_TAG_APP}"
  docker build --no-cache -f app.Dockerfile -t $DOCKER_TAG_APP --target $DOCKER_TARGET_APP .
  echo "Rebuilding ${DOCKER_TAG_ASSETS}"
  docker build --no-cache -f assets.Dockerfile -t $DOCKER_TAG_ASSETS .
else
  echo "Rebuilding ${DOCKER_TAG_APP}"
  docker build -f app.Dockerfile -t $DOCKER_TAG_APP --target $DOCKER_TARGET_APP .
  echo "Rebuilding ${DOCKER_TAG_ASSETS}"
  docker build -f assets.Dockerfile -t $DOCKER_TAG_ASSETS .
fi

echo "Spinning up containers"
if [ "$JANIS" == "on" ]; then
  # Env Vars for use in Janis
  export HOST_IP=$(ifconfig en0 | awk '$1 == "inet" {print $2}')
  export CMS_API="http://$HOST_IP:$JOPLIN_APP_HOST_PORT/api/graphql"
  export CMS_MEDIA="http://$HOST_IP:$JOPLIN_APP_HOST_PORT/media"
  export DOCKER_TAG_JANIS="janis:local"
  export JANIS_APP_HOST_PORT=3000

  docker-compose -f docker-compose.yml -f docker-compose.local_override.yml -f docker-compose.janis.yml up
else
  docker-compose -f docker-compose.yml -f docker-compose.local_override.yml up
fi
