#!/usr/bin/env bash

set -o errexit

# Get the heroku key. We eat stderr because the heroku cli will warn us that these tokens
# are short-lived. That's OK in our case because we're just running this locally.
HEROKU_KEY=$(heroku auth:token 2> /dev/null)

if [ "$REBUILD" == "on" ]; then

  export JOPLIN_APP_CONTAINER_NAME=joplin_app
  export JOPLIN_DB_CONTAINER_NAME=joplin_db
  export JOPLIN_ASSETS_CONTAINER_NAME=joplin_assets
  export JOPLIN_DB_PUBLIC_PORT=5433
  export JOPLIN_APP_PUBLIC_PORT=8000

  docker build --no-cache -f Dockerfile.base -t joplin-base .
  docker-compose -f docker-compose.local.yml up --build
elif [ "$MIGRATIONS_TEST" == "on" ]; then

  export JOPLIN_APP_CONTAINER_NAME=joplin_app_migration_test
  export JOPLIN_DB_CONTAINER_NAME=joplin_db_migration_test
  export JOPLIN_ASSETS_CONTAINER_NAME=joplin_assets_migration_test
  export JOPLIN_DB_PUBLIC_PORT=5434
  export JOPLIN_APP_PUBLIC_PORT=8000

  docker build -f Dockerfile.base -t joplin-base . --build-arg MIGRATIONS_TEST=on
  docker-compose -f docker-compose.local.yml up
else

  export JOPLIN_APP_CONTAINER_NAME=joplin_app
  export JOPLIN_DB_CONTAINER_NAME=joplin_db
  export JOPLIN_ASSETS_CONTAINER_NAME=joplin_assets
  export JOPLIN_DB_PUBLIC_PORT=5433
  export JOPLIN_APP_PUBLIC_PORT=8000

  docker build -f Dockerfile.base -t joplin-base .
  docker-compose -f docker-compose.local.yml up
fi
