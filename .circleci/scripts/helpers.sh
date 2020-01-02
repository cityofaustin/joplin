#!/usr/bin/env bash

########################################
# Declare Constants
# PIPELINE_NAME, ENV, APPNAME, SHA, DOCKER_TARGET, DOCKER_TAG_*
########################################
set -a # exports all assigned variables

# Heroku Pipeline Name
PIPELINE_NAME="joplin-pipeline"
PIPELINE_TEAM="odd"

# Get 7-character truncated SHA1 hash for git commit
SHA=${CIRCLE_SHA1:0:7}

# Use git branch to determine ENV and Heroku APPNAME
if [ "$CIRCLE_BRANCH" == "master" ]; then
  APPNAME="joplin-staging"
  DOCKER_TARGET="joplin-staging"
  DOCKER_TAG_1="cityofaustin/joplin-app:master-${SHA}"
  DOCKER_TAG_2="cityofaustin/joplin-app:master-latest"
elif [ "$CIRCLE_BRANCH" == "production" ]; then
  APPNAME="joplin"
  DOCKER_TARGET="joplin-prod"
  DOCKER_TAG_1="cityofaustin/joplin-app:production-${SHA}"
  DOCKER_TAG_2="cityofaustin/joplin-app:production-latest"
else
  # truncates to 30 characters for heroku app name length limitations
  # eliminate trailing dashes for heroku app name restrictions
  APPNAME="joplin-pr-$CIRCLE_BRANCH"; APPNAME=$(echo ${APPNAME:0:30} | awk '{print tolower($0)}' | sed -e 's/-*$//g')
  DOCKER_TARGET="joplin-review"
  DOCKER_TAG_1="cityofaustin/joplin-app:pr-${CIRCLE_BRANCH}-${SHA}"
  DOCKER_TAG_2="cityofaustin/joplin-app:pr-${CIRCLE_BRANCH}-latest"
fi
DOCKER_TAG_HEROKU=registry.heroku.com/$APPNAME/web

########################################
# Declare Functions
########################################

#
# Prints an indention based on the calling function
# $1 (string) name of the function
# $2 (int) level of indentation (1 is less, 5 is more)
# $3 (string) text
# Example: log "myfunc" 3 "My Message";
#          myfunc() --------------- My Message
# Example: log ${FUNCNAME[0]} 1 "My Message";
#       ${FUNCNAME[0]} holds the name of the function where it is being accessed from.
#
function log_base {
    RANGE=$(awk "BEGIN { print 5*${2} }")
    echo -n "${1}() "
    awk -v ORS=  "BEGIN { for (i = 1; i <= ${RANGE}; ++i) print \"-\" }" # leave ORS empty please
    echo -e " ${3}"
}

#
# Simply builds a noticeable header when parsing logs.
# This should help determine when our commands begin execution,
# and what branch is being affected by current deployment.
#
function print_header {
    echo ""
    echo ""
    echo "--------------------------------------------------------------"
    echo "   $1"
    echo "--------------------------------------------------------------"
    echo "  CIRCLE_BRANCH:              ${CIRCLE_BRANCH}"
    echo "  CIRCLE_PULL_REQUEST:        ${CIRCLE_PULL_REQUEST}"
    echo "  PIPELINE_TEAM:              ${PIPELINE_TEAM}"
    echo "  PIPELINE_NAME:              ${PIPELINE_NAME}"
    echo ""
}

# Returns "True" if our app name exists in heroku.
function app_exists {
    HEROKU_TEAM_APPS=$(heroku apps --team $PIPELINE_TEAM | grep $APPNAME)

    if [ "${HEROKU_TEAM_APPS}" != "" ]; then
        echo "true";
    else
        echo "false"
    fi;
}

# Returns "true" if our app has a postgresql db attached to it.
function app_database_attached {
  HEROKU_APP_DB_ATTACHED=$(heroku addons --app $APPNAME | grep postgresql)

  if [ ! -z "$HEROKU_APP_DB_ATTACHED" ]; then
    echo "true";
  else
    echo "false"
  fi;
}
