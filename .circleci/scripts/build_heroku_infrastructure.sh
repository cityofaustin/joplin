#!/usr/bin/env bash
set -eo pipefail
CURRENT_DIR=`dirname $BASH_SOURCE`
source $CURRENT_DIR/helpers.sh
log() { log_base "build_heroku_app" "$1" "$2"; }

# Creates App and Database in Heroku Pipeline if either don't already exist.

# Attaches postgresql database to heroku application
function attach_heroku_database {
    heroku addons:create heroku-postgresql:hobby-dev --version=12 --app $APPNAME
}

# Attaches redis cache to heroku application
function attach_heroku_redis {
    echo "todo"
#    todo
#    heroku addons:create heroku-postgresql:hobby-dev --version=10 --app $APPNAME
}

# If the review app exists, then check if database exists
APP_EXISTS=$(app_exists)
if [ "$APP_EXISTS" = "true" ]; then
  # If the review app exists, then add a database if it doesn't have one already
  log 2 "App $APPNAME already exists, tagging & checking if database exists.";
  APP_DB_EXISTS=$(app_database_attached)
  if [ "${APP_DB_EXISTS}" = "false" ]; then
      log 3 "No database detected, attaching new database to $APPNAME.";
      attach_heroku_database
      log 3 "Done attaching database."
  else
      log 2 "The database already exists."
  fi
else
  # Create a new Heroku review app, if the app doesn't already exist
  print_header "Build Heroku Review App"
  log 1 ">>> Deployment details:"
  log 1 "Deploying new app:         ${APPNAME}"
  log 1 "Into Pipeline:             ${PIPELINE_NAME}"

  # Create app with specified APPNAME
  heroku create $APPNAME --team $PIPELINE_TEAM

  # Add postgresql to the new app
  attach_heroku_database

  # Attach new app to pipeline (assign review (PR) stage):
  heroku pipelines:add $PIPELINE_NAME --app $APPNAME --stage review
fi
