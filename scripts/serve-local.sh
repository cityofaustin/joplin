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
export DOCKER_TAG_APP="joplin_app:local"
export DOCKER_TAG_ASSETS="joplin_assets:local"
export DOCKER_TARGET_APP=joplin-local

# Stop any existing joplin containers that might still be running
echo "Stopping any $COMPOSE_PROJECT_NAME containers that might still be running"
stop_project_containers $COMPOSE_PROJECT_NAME

if [ "$HARD_REBUILD" == "on" ]; then
  echo 'HARD_REBUILD="on": Rebuilding containers without cache'
  echo "Rebuilding ${DOCKER_TAG_APP}"
  docker build --no-cache -f Dockerfile.app -t $DOCKER_TAG_APP --target $DOCKER_TARGET_APP .
  echo "Rebuilding ${DOCKER_TAG_ASSETS}"
  docker build --no-cache -f Dockerfile.assets -t $DOCKER_TAG_ASSETS .
else
  echo "Rebuilding ${DOCKER_TAG_APP}"
  docker build -f Dockerfile.app -t $DOCKER_TAG_APP --target $DOCKER_TARGET_APP .
  echo "Rebuilding ${DOCKER_TAG_ASSETS}"
  docker build -f Dockerfile.assets -t $DOCKER_TAG_ASSETS .
fi

echo "Spinning up containers"
docker-compose -f docker-compose.yml -f docker-compose.local_override.yml up
