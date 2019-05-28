#!/usr/bin/env bash
set -eo pipefail
CURRENT_DIR=`dirname $BASH_SOURCE`
source $CURRENT_DIR/helpers.sh
log() { log_base "release" "$1" "$2"; }

print_header "Releasing Image"

# Release the container to heroku
heroku container:release web --app $APPNAME
