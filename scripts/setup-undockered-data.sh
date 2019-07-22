#!/usr/bin/env bash

set -o errexit
CURRENT_DIR=`dirname $BASH_SOURCE`

# This script runs data operations for an undockerized Joplin instance that
# would otherwise have occured in docker-entrypoint.sh

# Migrate
pipenv run $CURRENT_DIR/../joplin/manage.py migrate --noinput

if [ "$LOAD_DATA" == "on" ]; then
  # Load backup data
  pipenv run $CURRENT_DIR/../joplin/manage.py loaddata $CURRENT_DIR/../joplin/db/system-generated/seeding.datadump.json
fi

# Load test admin
pipenv run $CURRENT_DIR/../joplin/manage.py loaddata $CURRENT_DIR/../joplin/db/system-generated/local_admin_user.json
