#!/usr/bin/env bash

set -o errexit

# Allows us to use BUILDKIT features like adding a --target to docker build
# Only works for "docker build" not "docker-compose ... --build"
export DOCKER_BUILDKIT=1

# Get the heroku key. We eat stderr because the heroku cli will warn us that these tokens
# are short-lived. That's OK in our case because we're just running this locally.
HEROKU_KEY=$(heroku auth:token 2> /dev/null)

if [ "$REBUILD" == "on" ]; then
  echo "disabled for now"
  # export COMPOSE_PROJECT_NAME=joplin
  # export JOPLIN_DB_PUBLIC_PORT=5433
  # export JOPLIN_APP_PUBLIC_PORT=8000
  # export TARGET=joplin-local
  #
  # docker build --no-cache -f Dockerfile.base -t joplin-base .
  # docker-compose -f docker-compose.local.yml -f docker-compose.local_override.yml up --build
elif [ "$MIGRATION_TEST" == "on" ]; then
  # Env Vars for use in Joplin
  export JOPLIN_DB_HOST_PORT=5434
  export JOPLIN_DB_CONTAINER_PORT=5432
  export JOPLIN_APP_HOST_PORT=8001
  export JOPLIN_APP_CONTAINER_PORT=80

  # Build Args for use during build process
  export COMPOSE_PROJECT_NAME=joplin_migration_test
  export DOCKER_IMAGE_APP="joplin_app:migration-test"
  export DOCKER_TARGET_APP=joplin-migration-test
  export GITHUB_URL="https://github.com/cityofaustin/joplin.git#1836-migration-script"

  if [ "$RESTART" == "on" ]; then
    echo "Stopping existing containers"
    docker-compose build -f docker-compose.yml stop
  fi

  echo "Rebuilding ${DOCKER_IMAGE_APP} from ${GITHUB_URL}"
  docker build -f Dockerfile.app -t $DOCKER_IMAGE_APP --target $DOCKER_TARGET_APP $GITHUB_URL
  echo "Spinning up migration-test containers"
  docker-compose build -f docker-compose.yml up
else
  # Env Vars for use within Joplin
  export JOPLIN_DB_HOST_PORT=5433
  export JOPLIN_DB_CONTAINER_PORT=5432
  export JOPLIN_APP_HOST_PORT=8000
  export JOPLIN_APP_CONTAINER_PORT=80

  # Build Args for use during build process
  export COMPOSE_PROJECT_NAME=joplin
  export DOCKER_IMAGE_APP="joplin_app:local"
  export DOCKER_IMAGE_ASSETS="joplin_assets:local"
  export DOCKER_TARGET_APP=joplin-local

  if [ "$RESTART" == "on" ]; then
    echo "Stopping existing containers"
    docker-compose -f docker-compose.yml -f docker-compose.local_override.yml stop
  fi

  echo "Rebuilding ${DOCKER_IMAGE_APP}"
  docker build -f Dockerfile.app -t $DOCKER_IMAGE_APP --target $DOCKER_TARGET_APP .
  echo "Rebuilding ${DOCKER_IMAGE_ASSETS}"
  docker build -f Dockerfile.assets -t $DOCKER_IMAGE_ASSETS .
  echo "Spinning up containers"
  docker-compose -f docker-compose.yml -f docker-compose.local_override.yml up
fi
