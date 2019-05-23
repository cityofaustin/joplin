#!/usr/bin/env bash
set -eo pipefail
CURRENT_DIR=`dirname $BASH_SOURCE`
source $CURRENT_DIR/helpers.sh
log() { log_base "migrate" $1 $2; }

print_header "Running Database Migration"

# Manually run entrypoint script
log 0 "Migrating data for App: ${APPNAME}";
heroku run --app $APPNAME -- /app/docker-entrypoint.sh
