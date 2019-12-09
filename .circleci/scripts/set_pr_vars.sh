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

python3 $CURRENT_DIR/../vars/heroku_pr_vars.py $APPNAME
