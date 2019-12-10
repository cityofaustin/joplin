#!/usr/bin/env bash
set -eo pipefail
CURRENT_DIR=`dirname $BASH_SOURCE`
source $CURRENT_DIR/helpers.sh
log() { log_base "migrate" "$1" "$2"; }

print_header "Running Database Migration"

# Manually run entrypoint script
python3 $CURRENT_DIR/check_app_status.py $APPNAME
log 0 "Migrating data for App: ${APPNAME}";
heroku run -x --app $APPNAME -- /app/docker-entrypoint.sh
