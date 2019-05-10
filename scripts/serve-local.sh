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
  export COMPOSE_PROJECT_NAME=joplin_migration_test
  export JOPLIN_DB_PUBLIC_PORT=5434
  export JOPLIN_APP_PUBLIC_PORT=8001
  export TARGET=joplin-migration-test
  export GITHUB_URL="https://github.com/cityofaustin/joplin.git#1836-migration-script"

  docker build -f Dockerfile.app -t migration-test --target $TARGET $GITHUB_URL
  docker-compose build -f docker-compose.yml -f docker-compose.migration_test_override.yml up
else
  export COMPOSE_PROJECT_NAME=joplin
  export JOPLIN_DB_PUBLIC_PORT=5433
  export JOPLIN_APP_PUBLIC_PORT=8000
  export TARGET=joplin-local

  docker build -f Dockerfile.app -t local --target $TARGET .
  docker-compose -f docker-compose.yml -f docker-compose.local_override.yml up
fi
