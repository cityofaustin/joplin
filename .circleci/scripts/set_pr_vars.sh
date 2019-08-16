#!/usr/bin/env bash
set -eo pipefail
CURRENT_DIR=`dirname $BASH_SOURCE`
source $CURRENT_DIR/helpers.sh
log() { log_base "set_pr_vars" "$1" "$2"; }

# Add or update environment variables for review app
# Environment variables for staging and production are handled manually within Heroku Console
# Vars prefixed with "CI_" are sourced from circleci
# Suppress stdout with "> /dev/null" to hide display of sensitive variables
log 1 "Adding environment variables to Heroku App: $APPNAME"

heroku config:set   \
  APPLICATION_NAME=$APPNAME \
  AWS_S3_KEYID=$AWS_ACCESS_KEY_ID \
  AWS_S3_ACCESSKEY=$AWS_SECRET_ACCESS_KEY \
  AWS_S3_USER=$CI_AWS_S3_USER \
  AWS_S3_BUCKET=joplin-austin-gov-static \
  AWS_S3_BUCKET_ARCHIVE=$CI_AWS_S3_BUCKET_ARCHIVE \
  AWS_S3_BUCKET_ARCHIVE_LOCATION=$CI_AWS_S3_BUCKET_ARCHIVE_LOCATION \
  CIRCLE_BRANCH=$CIRCLE_BRANCH \
  DEBUG=1 \
  HEROKU_JANIS_APP_NAME="janis-staging" \
  JANIS_URL="https://janis-staging.herokuapp.com" \
  STYLEGUIDE_URL="https://cityofaustin.github.io/digital-services-style-guide" \
  --app $APPNAME > /dev/null
