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
if [ "$NO_STOP" != "on" ]; then
  echo "Stopping any $COMPOSE_PROJECT_NAME containers that might still be running"
  stop_project_containers $COMPOSE_PROJECT_NAME
fi

# Aside from the database dropping step, RELOAD_DATA does the same thing as LOAD_DATA
if [ ! -z "$RELOAD_DATA" ]; then
  export LOAD_DATA=$RELOAD_DATA
  export DROP_DB="on"
fi

if [ "$DEBUG_TOOLBAR" == "on" ];
then
  export DEBUG_TOOLBAR=1
else
  export DEBUG_TOOLBAR=0
fi

if [ "$UNDOCK" == "on" ]; then
  export NO_BUILD="on"
fi

if [ "$HARD_REBUILD" == "on" ]; then
  unset NO_BUILD
fi

# Delete old database containers for HARD_REBUILDs or RELOADs
if [ "$HARD_REBUILD" == "on" ] || [ "$DROP_DB" == "on" ]; then
  echo "Deleting old joplin_db containes"
  docker ps -aq -f name=joplin_db_1 | while read CONTAINER ; do docker rm -f $CONTAINER ; done
fi

if [ "$NO_BUILD" != "on" ]; then
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
fi

if [ "$UNDOCK" != "on" ]; then
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
else
  # Required vars that are added in docker-compose.yml
  export STYLEGUIDE_URL="https://cityofaustin.github.io/digital-services-style-guide"
  export DEBUG=1

  # Django will access DATABASE_URL from HOST, not a container in the same network
  export DATABASE_URL="postgres://joplin@127.0.0.1:${JOPLIN_DB_HOST_PORT}/joplin"

  # Only run containers for db and assets
  docker-compose -f docker-compose.yml -f docker-compose.local_override.yml up -d db assets

  export DEPLOYMENT_MODE=LOCAL
  pipenv run sh $CURRENT_DIR/../docker-entrypoint.sh
  pipenv run $CURRENT_DIR/../joplin/manage.py runserver 0.0.0.0:$JOPLIN_APP_HOST_PORT
fi
