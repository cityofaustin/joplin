#!/usr/bin/env bash

set -o errexit

if [ "$REBUILD_PIPENV" == "on" ]; then
  pipenv --rm
  pipenv install --requirements deploy/requirements.txt
fi

CURRENT_DIR=`dirname $BASH_SOURCE`
UNDOCK=on sh $CURRENT_DIR/serve-local.sh
