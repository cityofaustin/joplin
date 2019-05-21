#!/usr/bin/env bash

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
function log {
    RANGE=$(awk "BEGIN { print 5*${2} }")
    echo -n "${1} "
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


# Determine ENV by your git branch
function get_env {
  if [ "$CIRCLE_BRANCH" == "master" ]; then
    echo "staging"
  elif [ "$CIRCLE_BRANCH" == "production" ]; then
    echo "prod"
  else
    echo "dev"
  fi
}

# Get 7-character truncated SHA1 hash for git commit
function get_sha {
  SHA=${CIRCLE_SHA1:0:7}
  echo $SHA
}

# Turn the branch name into the app name in Heroku
function get_heroku_appname {
  case $CIRCLE_BRANCH in
    production)
      APPNAME="joplin"
      ;;
    master)
      APPNAME="joplin-staging"
      ;;
    *)
      APPNAME="joplin-dev-$CIRCLE_BRANCH"
    ;;
  esac

  # Output results for logging
  echo $APPNAME
}

# Returns "true" if a given app name has a postgresql db attached to it.
function app_database_attached {
  HEROKU_APP_DB_ATTACHED=$(heroku addons --app $1 | grep postgresql)

  if [ ! -z "$HEROKU_APP_DB_ATTACHED" ]; then
    echo "true";
  else
    echo "false"
  fi;
}
