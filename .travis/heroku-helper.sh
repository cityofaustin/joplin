#!/usr/bin/env bash

# Tag used for testing
export TRAVIS_CI_TEST_TAG="travis-ci-internal-test"

#
# Pipeline Variables
# These determine the exact pipeline in the heroku account where new PR (review apps) are created.
# It also determines which "team" group will be used.
#

# The team name (a sort of sub-account in heroku)
export PIPELINE_TEAM=$PIPELINE_TEAM_DEFAULT
# The name of the pipeline in the team account.
export PIPELINE_NAME=$PIPELINE_NAME_DEFAULT

#
# Colors
#
export RED='\033[0;31m'
export NC='\033[0m' # No Color

#
# Prints error message and stops deployment by returing exit 1
# $1 (string) - Error message to display
# Example: helper_halt_deployment "File not found"
#
function helper_halt_deployment {
    echo -e "--------------------------------------------------------------"
    echo -e "${RED}FATAL ERROR:${NC}"
    echo -e "${1}"
    echo -e "--------------------------------------------------------------"
    travis_terminate 1;
}

#
# Helps validate branch name (or stops deployment if no branch specified)
# $1 (string) The name of the function callling this method
# $2 (string) the name of the branch
# Example: helper_internal_validation "heroku_test" "production"
#
function helper_internal_validation {
    # Show message if this is an internal test
    if [ "$2" = "${TRAVIS_CI_TEST_TAG}" ]; then
        echo "  > $1(): Ready to execute.";
        return 1
    fi;

    # Output error if no branch is specified.
    if [ "$2" = "" ]; then
        helper_halt_deployment "$1(): Branch name required (ie: '$1 staging'). Halting deployment.";
    fi;

    joplin_log $1 1 "We have a working branch: $2";
    return 0
}

#
# Simply builds a noticeable header when parsing logs.
# This should help determine when our commands begin execution,
# and what branch is being affected by current deployment.
#
function joplin_print_header {
    echo ""
    echo ""
    echo "--------------------------------------------------------------"
    echo "   $1"
    echo "--------------------------------------------------------------"
    echo "  TRAVIS_BRANCH:              ${TRAVIS_BRANCH}"
    echo "  TRAVIS_PULL_REQUEST:        ${TRAVIS_PULL_REQUEST}"
    echo "  TRAVIS_PULL_REQUEST_BRANCH: ${TRAVIS_PULL_REQUEST_BRANCH}"
    echo "  PIPELINE_TEAM:              ${PIPELINE_TEAM}"
    echo "  PIPELINE_NAME:              ${PIPELINE_NAME}"
    echo ""
}

#
# Returns "True" if a given app name exists in heroku.
# $1 (string) The name of the app (ie. joplin-staging, joplin-pr-160)
#
function joplin_app_exists {
    HEROKU_TEAM_APPS=$(heroku apps --team $PIPELINE_TEAM | grep $1)

    if [ "${HEROKU_TEAM_APPS}" != "" ]; then
        echo "true";
    else
        echo "false"
    fi;
}

#
# Returns "True" if a given app name has a postgresql db attached to it.
#
function joplin_app_database_attached {
    HEROKU_APP_DB_ATTACHED=$(heroku addons --app $1 | grep postgresql)

    if [ "${HEROKU_APP_DB_ATTACHED}" != "" ]; then
        echo "true";
    else
        echo "false"
    fi;
}

#
# Prints an indention based on the calling function
# $1 (string) name of the function
# $2 (int) level
# $3 (string) text
# Example: joplin_log "myfunc" 3 "My Message";
# Example: joplin_log ${FUNCNAME[0]} 1 "My Message";
#       ${FUNCNAME[0]} holds the name of the function where it is being accessed from.
#
function joplin_log {
    RANGE=$(awk "BEGIN { print 5*${2} }")
    echo -n "${1}() "
    awk -v ORS=  "BEGIN { for (i = 1; i <= ${RANGE}; ++i) print \"-\" }" # leave ORS empty please
    echo -e " ${3}"
}

#
# Returns "true" if $1 is a numeric value, otherwise returns "false".
# $1 (string) - The string to be tested as numeric.
#
function joplin_is_numeric {
    REGEX_NUMERIC='^[0-9]+$'
    if ! [[ "${1}" =~ $REGEX_NUMERIC ]] ; then
        echo "false";    # Not a number
    else
        echo "true";    # We have a number
    fi
}

#
# Attaches a database to an application.
# $1 (string) The name of the app to create.
# $2 (string) The name of the pipeline
#
function joplin_attach_heroku_database {
    # The new app name
    HEROKU_NEW_APP_NAME=$1

    # Add postgresql to the new app.
    heroku addons:create heroku-postgresql:hobby-dev --version=10 --app $HEROKU_NEW_APP_NAME
}

#
# Turn the branch name into the app name in Heroku
#
function joplin_resolve_heroku_appname {

    # Turn the branch name into the application name we need
    # production:   joplin
    # master:       joplin-staging

    # If there is a pull request number, then it must be a PR branch

    if [ "${TRAVIS_PULL_REQUEST}" != "false" ]; then
        APPNAME="joplin-staging-pr-${TRAVIS_PULL_REQUEST}"

    # If not, then proceed with the regular branch name (master, production)
    else
        case $TRAVIS_BRANCH in
            production)
                APPNAME="joplin"
                ;;
            master)
                APPNAME="joplin-staging"
                ;;
            *)
                helper_halt_deployment "The app name could not be resolved for branch: '${TRAVIS_BRANCH}'"
            ;;
        esac
    fi;

    # Output results for logging
    echo "${APPNAME}"
}
