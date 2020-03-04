#!/usr/bin/env bash
set -o errexit
CURRENT_DIR=`dirname $BASH_SOURCE`
source $CURRENT_DIR/docker-helpers.sh

# function clean_up {
#   if [ -f "$TMP_DATADUMP" ]; then
#     echo "#### Deleting intermediate temp datadump"
#     rm $TMP_DATADUMP
#   fi
#   if [ -f "$PLACEHOLDER_DATADUMP" ]; then
#     echo "#### Deleting intermediate temp datadump"
#     rm $PLACEHOLDER_DATADUMP
#   fi
#   if [ ! -z "$COMPOSE_PROJECT_NAME" ]; then
#     echo "#### Shutting down containers safely"
#     stop_project_containers $COMPOSE_PROJECT_NAME
#   fi
# }
# trap clean_up EXIT

function get_heroku_datadump {
  APPNAME=$1
  # Replace all user passwords with default admin test password
  # TODO: once prod has scripts/export_heroku_data.sh, run sanitation script on production container itself
  heroku run -xa $APPNAME python ./joplin/manage.py dumpdata --exclude=wagtailcore.GroupCollectionPermission --indent 2 --natural-foreign --natural-primary -- | \
    python ./scripts/remove_logs_from_json_stream.py | \
    jq '(.[] | select(.model == "users.user") | .fields.password) |= "pbkdf2_sha256$150000$GJQ1UoZlgrC4$Ir0Uww/i9f2VKzHznU4B1uaHbdCxRnZ69w12cIvxWP0="' \
    > $TMP_DATADUMP ; sleep 100
}

function make_placeholder_datadump {
  echo "Generating placeholder datadump"
  # Excluding wagtailcore.GroupCollectionPermission because of IntegrityError issues
  # see: https://docs.djangoproject.com/en/2.2/topics/serialization/#natural-keys for details
  docker exec -it ${COMPOSE_PROJECT_NAME}_app_1 python joplin/manage.py dumpdata --exclude=wagtailcore.GroupCollectionPermission --indent 2 --natural-foreign --natural-primary | \
    python ./scripts/remove_logs_from_json_stream.py \
    > $PLACEHOLDER_DATADUMP
}

# Env Vars for use in Joplin
export JOPLIN_DB_HOST_PORT=5434
export JOPLIN_DB_CONTAINER_PORT=5432
export JOPLIN_APP_HOST_PORT=8000
export JOPLIN_APP_CONTAINER_PORT=80
export JANIS_URL=http://localhost:3000
export DATABASE_URL="postgres://joplin@db:${JOPLIN_DB_CONTAINER_PORT}/joplin"
export DEBUG_TOOLBAR=0

# Build Args for use during build process
export COMPOSE_PROJECT_NAME=joplin_migration_test
export TMP_DATADUMP=$CURRENT_DIR/../joplin/db/system-generated/tmp.datadump.json
export PLACEHOLDER_DATADUMP=$CURRENT_DIR/../joplin/db/system-generated/placeholder.datadump.json

# If loading prod data, then your db must be built using prod migrations from the prod joplin-app image
# docker-compose.migration_test_override.yml will replace any production specific settings/variables with local settings
# Must have herokucli installed and be authenticated to access production joplin
case "${SOURCE}" in
  prod)
    export SOURCED_FROM="PROD"
    export DOCKER_TAG_APP="cityofaustin/joplin-app:production-latest"
    if [ "${USE_PRIOR_DATADUMP}" == "on" ]; then
      export LOAD_DATA="prod"
    else
      export LOAD_DATA="new_datadump"
      echo "Pulling datadump from Production"
      get_heroku_datadump joplin
    fi
  ;;
  staging)
    export SOURCED_FROM="STAGING"
    export DOCKER_TAG_APP="cityofaustin/joplin-app:master-latest"
    if [ "${USE_PRIOR_DATADUMP}" == "on" ]; then
      export LOAD_DATA="staging"
    else
      export LOAD_DATA="new_datadump"
      echo "Pulling datadump from Staging"
      get_heroku_datadump joplin-staging
    fi
  ;;
  dummy)
    export SOURCED_FROM="LAST_DUMMY_DATADUMP"
    export DOCKER_TAG_APP="cityofaustin/joplin-app:master-latest"
    export LOAD_DATA="dummy"
  ;;
  *)
    echo "Error: [${SOURCE}] is not a valid SOURCE"
    exit 1
  ;;
esac

# Optionally plug in your own DOCKER_TAG_DB_BUILD to build a db with data and migrations from a different branch or build
export DOCKER_TAG_APP=${DOCKER_TAG_DB_BUILD:=$DOCKER_TAG_APP}
export DOCKER_TARGET_APP=joplin-migration-test

echo "######################"
echo "Step 1: Create db from $DOCKER_TAG_APP"
echo "######################"
echo "#### Builds a database environment from $DOCKER_TAG_APP"
echo "#### Loads migrations and data from $DOCKER_TAG_APP"

echo "#### Removing local ${COMPOSE_PROJECT_NAME} containers"
stop_project_containers joplin
delete_project_containers $COMPOSE_PROJECT_NAME

echo "#### Pulling ${DOCKER_TAG_APP} from dockerhub"
docker pull $DOCKER_TAG_APP
echo "#### Spinning up joplin-app and joplin_db containers to LOAD_DATA from $DOCKER_TAG_APP"
docker-compose -f docker-compose.yml -f docker-compose.migration_test_override.yml up -d

echo "#### Running old migrations from $DOCKER_TAG_APP and loading data"
docker logs ${COMPOSE_PROJECT_NAME}_app_1 -f
docker wait ${COMPOSE_PROJECT_NAME}_app_1
# Stop process if our entrypoint.sh errored out on docker-compose
if [[ $(docker inspect ${COMPOSE_PROJECT_NAME}_app_1 --format='{{.State.ExitCode}}') == '1' ]]; then
  exit 1
fi
echo "#### $DOCKER_TAG_APP migration and data loading completed successfully"
echo "#### $DOCKER_TAG_APP joplin-app container shutting down"

echo "######################"
echo "Step 2: Run new migrations on old db"
echo "######################"

# Env Vars for use in Janis
export HOST_IP=$(ifconfig en0 | awk '$1 == "inet" {print $2}')
export CMS_API="http://$HOST_IP:$JOPLIN_APP_HOST_PORT/api/graphql"
export CMS_MEDIA="http://$HOST_IP:$JOPLIN_APP_HOST_PORT/media"
export DOCKER_TAG_JANIS="janis:local"
export JANIS_APP_HOST_PORT=3000

# Env Vars for use in Joplin
export JANIS_URL="http://localhost:${JANIS_APP_HOST_PORT}"
export DATABASE_IPADDRESS=$(docker inspect --format '{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}' "${COMPOSE_PROJECT_NAME}_db_1")
export DATABASE_URL="postgres://joplin@${DATABASE_IPADDRESS}:${JOPLIN_DB_CONTAINER_PORT}/joplin"

# Data already loaded in step 1. Don't load data again for this step
unset LOAD_DATA

# Build Args for use during build process
export DOCKER_TAG_APP="joplin-app:local"
export DOCKER_TARGET_APP=joplin-local

echo "#### Rebuilding ${DOCKER_TAG_APP}"
# DOCKER_BUILDKIT=1 Allows us to use BUILDKIT features like adding a --target to docker build
DOCKER_BUILDKIT=1 docker build -f app.Dockerfile -t $DOCKER_TAG_APP --target $DOCKER_TARGET_APP .

docker-compose -f docker-compose.yml -f docker-compose.migration_test_override.yml up -d
echo "#### Running new migrations from $DOCKER_TAG_APP"
docker logs ${COMPOSE_PROJECT_NAME}_app_1 -f
docker wait ${COMPOSE_PROJECT_NAME}_app_1

if [ "$JANIS" == "on" ]; then
  echo "#### Spinning up joplin-app and janis containers to run a test server"
  docker-compose -f docker-compose.yml -f docker-compose.janis.yml up -d
else
  echo "#### Spinning up joplin-app containers to run a test server"
  docker-compose -f docker-compose.yml up -d
fi

# Make placeholder datadump before user testing manipulates data.
# After user confirms that data is okay, then the placeholder_datadump
# will be committed as the real datadump.
# We don't run this step with "dummy", because we do want to manipulate dummy data
# during testing.
case "${SOURCE}" in
  prod|staging)
    make_placeholder_datadump
  ;;
esac

echo "######################"
echo "Step 3: The Manual One"
echo "######################"
echo "#### Check that your migration changes work for both Janis and the Joplin Authoring Interface."
echo "#### Joplin URL: http://localhost:${JOPLIN_APP_HOST_PORT}/admin"
if [ "$JANIS" == "on" ]; then
  echo "#### Janis URL: ${JANIS_URL}"
else
  echo "#### To test that Janis runs with your migration changes, run a local Janis instance."
  echo "#### Make sure that your Janis environment variables point to this Joplin."
  echo "#### CMS_API   should = $CMS_API"
  echo "#### CMS_MEDIA should = $CMS_MEDIA"
  echo "######################"
fi

function handle_input {
  echo "#### Is it all good? Enter y/n"
  echo "#### If you enter n, the story ends, the ${COMPOSE_PROJECT_NAME} containers will be stopped, you wake up in your bed, and you believe whatever you want to believe."
  echo "#### If you enter y, then congratulations, we'll rewrite joplin/db/system-generated/seeding.datadump.json with your latest migration changes."
  read answer
  if [ "$answer" == "y" ]; then
    echo "#### Glad that worked. We'll save a new migration_datadump for you."

    case "${SOURCE}" in
      prod)
        DATADUMP_JSON=$CURRENT_DIR/../joplin/db/system-generated/prod.datadump.json
        DATADUMP_METADATA=$CURRENT_DIR/../joplin/db/system-generated/prod_datadump_metadata.txt
      ;;
      staging)
        DATADUMP_JSON=$CURRENT_DIR/../joplin/db/system-generated/staging.datadump.json
        DATADUMP_METADATA=$CURRENT_DIR/../joplin/db/system-generated/staging_datadump_metadata.txt
      ;;
      dummy)
        DATADUMP_JSON=$CURRENT_DIR/../joplin/db/system-generated/dummy.datadump.json
        DATADUMP_METADATA=$CURRENT_DIR/../joplin/db/system-generated/dummy_datadump_metadata.txt
      ;;
    esac

    if [ "$SOURCE" == "dummy" ]; then
      make_placeholder_datadump
    fi

    # Save placeholder to datadump json
    mv $PLACEHOLDER_DATADUMP $DATADUMP_JSON

    # Handle timestamp logging for metadata file
    CURRENT_TIMESTAMP="\"$(date '+%Y-%m-%d--%H-%M-%S')\""
    function get_last_sync_timestamp {
      if [ "$USE_PRIOR_DATADUMP" == "on" ]; then
        # Use timestamp from the last sync from prod if the data was sourced from a prior datadump
        echo $(grep -w "TIMESTAMP OF LAST SYNC" $DATADUMP_METADATA | awk -F ': ' '{print $2}')
      else
        # If this current datadump was sourced from prod or staging, then use CURRENT_TIMESTAMP
        echo $CURRENT_TIMESTAMP
      fi
    }
    # Read timestamp of last sync before we overwrite the old metadata file
    LAST_SYNC_TIMESTAMP=$(get_last_sync_timestamp)

    # Write new metadata file
    touch $DATADUMP_METADATA
    > $DATADUMP_METADATA

    # Appends line to datadump_metadata.txt file
    function append {(
      echo $1 >> $DATADUMP_METADATA
    )}

    # Will execute a psql query and export its value.
    # sed $'s/\x0D//g' gets rid of \r character for both linux and MacOS.
    # Format your psql query in such a way that it only expects to return a single value.
    function exec_psql_query {(
      PSQL_QUERY=$1
      echo $(docker exec -it ${COMPOSE_PROJECT_NAME}_db_1 psql postgres://joplin@127.0.0.1:${JOPLIN_DB_CONTAINER_PORT}/joplin -qtA -c "$1" | sed $'s/\x0D//g')
    )}

    append "TIMESTAMP: $CURRENT_TIMESTAMP"
    append "TIMESTAMP OF LAST SYNC: $LAST_SYNC_TIMESTAMP"
    append "LATEST_MIGRATION: \"$(exec_psql_query "select name from django_migrations order by id desc limit 1;")\""
    append "LATEST_BASE_MIGRATION: \"$(exec_psql_query "select name from django_migrations where app='base' order by id desc limit 1;")\""
    append "TOTAL_MIGRATIONS: $(exec_psql_query "select count(*) from django_migrations;")"
    append "TOTAL_BASE_MIGRATIONS: $(exec_psql_query "select count(*) from django_migrations where app='base';")"
    append "BRANCH: \"$(git rev-parse --abbrev-ref HEAD)\""

    exit 0
  elif [ "$answer" == "n" ]; then
    echo "#### Sorry to hear that. Cleaning up all ${COMPOSE_PROJECT_NAME} containers. Feel free to try again later."
    exit 0
  else
    echo "#### You entered [$answer], which is neither 'y' nor 'n'."
    handle_input
  fi
}

handle_input
