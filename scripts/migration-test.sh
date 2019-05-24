#!/usr/bin/env bash
set -o errexit
CURRENT_DIR=`dirname $BASH_SOURCE`
source $CURRENT_DIR/docker-helpers.sh

# Allows us to use BUILDKIT features like adding a --target to docker build
# Only works for "docker build" not "docker-compose ... --build"
export DOCKER_BUILDKIT=1

# Env Vars for use in Joplin
export JOPLIN_DB_HOST_PORT=5434
export JOPLIN_DB_CONTAINER_PORT=5432
export JOPLIN_APP_HOST_PORT=8001
export JOPLIN_APP_CONTAINER_PORT=80
export JANIS_URL=http://localhost:3000
export DATABASE_URL="postgres://joplin@db:${JOPLIN_DB_CONTAINER_PORT}/joplin"
export LOAD_DATA="on"

# Build Args for use during build process
export COMPOSE_PROJECT_NAME=joplin_migration_test
export DB_CREATION_DOCKER_TAG="cityofaustin/joplin-app:master-latest"
export DOCKER_TARGET_APP=joplin-migration-test

echo "######################"
echo "Step 1: Create db from $DB_CREATION_DOCKER_TAG"
echo "######################"
echo "Builds a database environment from $DB_CREATION_DOCKER_TAG"
echo "Loads migrations and data from $DB_CREATION_DOCKER_TAG"

echo "Removing local ${COMPOSE_PROJECT_NAME} containers"
delete_project_containers $COMPOSE_PROJECT_NAME

echo "Pulling ${DB_CREATION_DOCKER_TAG} from dockerhub"
docker pull $DB_CREATION_DOCKER_TAG
echo "Spinning up joplin-app and joplin_db containers"
docker-compose -f docker-compose.yml -f docker-compose.migration_test_override.yml up -d

echo "Running old migrations from $DB_CREATION_DOCKER_TAG and loading data"
docker logs ${COMPOSE_PROJECT_NAME}_app_1 -f
docker wait ${COMPOSE_PROJECT_NAME}_app_1
echo "$DB_CREATION_DOCKER_TAG migration and data loaded completed successfully"
echo "$DB_CREATION_DOCKER_TAG joplin-app container shutting down"

echo "######################"
echo "Step 2: Run new migrations on old db"
echo "######################"

# Env Vars for use in Janis
export HOST_IP=$(ifconfig en0 | awk '$1 == "inet" {print $2}')
export CMS_API="http://$HOST_IP:$JOPLIN_APP_HOST_PORT/api/graphql"
export CMS_MEDIA="http://$HOST_IP:$JOPLIN_APP_HOST_PORT/media"
export DOCKER_TAG_JANIS="janis:local"
export JANIS_APP_HOST_PORT=3001

# Env Vars for use in Joplin
export JANIS_URL="http://localhost:${JANIS_APP_HOST_PORT}"
export DATABASE_IPADDRESS=$(docker inspect --format '{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}' "${COMPOSE_PROJECT_NAME}_db_1")
export DATABASE_URL="postgres://joplin@${DATABASE_IPADDRESS}:${JOPLIN_DB_CONTAINER_PORT}/joplin"
export LOAD_DATA="off"

# Build Args for use during build process
export DOCKER_TAG_APP="joplin-app:local"
export DOCKER_TARGET_APP=joplin-local

echo "Rebuilding ${DOCKER_TAG_APP}"
docker build -f app.Dockerfile -t $DOCKER_TAG_APP --target $DOCKER_TARGET_APP .

echo "Spinning up joplin-app and janis containers"
docker-compose -f docker-compose.yml -f docker-compose.janis.yml up -d

echo "######################"
echo "Step 3: The Manual One"
echo "######################"
echo "Check that your migration changes work for both Janis and the Joplin Authoring Interface."
echo "Janis URL: ${JANIS_URL}"
echo "Joplin URL: http://localhost:${JOPLIN_APP_HOST_PORT}/admin"

function handle_input {
  echo "Is it all good? Enter y/n"
  echo "If you enter n, the story ends, the ${COMPOSE_PROJECT_NAME} containers will be stopped, you wake up in your bed, and you believe whatever you want to believe."
  echo "If you enter y, then congratulations, we'll rewrite joplin/db/system-generated/[migration].datadump.json with your latest migration changes."
  read answer
  if [ "$answer" == "y" ]; then
    echo "Glad that worked. We'll create a new migration_datadump for you."

    # Get name of latest migration from database
    LATEST_MIGRATION=$(psql postgres://joplin@127.0.0.1:${JOPLIN_DB_HOST_PORT}/joplin -qtA -c 'select name from django_migrations order by id desc limit 1;')
    NEW_MIGRATION_DATADUMP="${LATEST_MIGRATION}.datadump.json"

    # Remove old migration datadump
    OLD_MIGRATION_DATADUMP=$CURRENT_DIR/../joplin/db/system-generated/*.datadump.json
    if [ ! -z $OLD_MIGRATION_DATADUMP ]; then rm $OLD_MIGRATION_DATADUMP; fi

    # Build new migration datadump
    docker exec -it ${COMPOSE_PROJECT_NAME}_app_1 python joplin/manage.py dumpdata > ./joplin/db/system-generated/$NEW_MIGRATION_DATADUMP

    stop_project_containers $COMPOSE_PROJECT_NAME
    exit 0
  elif [ "$answer" == "n" ]; then
    echo "Sorry to hear that. Cleaning up all ${COMPOSE_PROJECT_NAME} containers. Feel free to try again later."
    stop_project_containers $COMPOSE_PROJECT_NAME
    exit 0
  else
    echo "You entered [$answer], which is neither 'y' nor 'n'."
    handle_input
  fi
}

handle_input
