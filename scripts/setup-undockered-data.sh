#!/usr/bin/env bash

set -o errexit
CURRENT_DIR=`dirname $BASH_SOURCE`

# Migrate
pipenv run $CURRENT_DIR/../joplin/manage.py migrate --noinput

# Load backup data
pipenv run $CURRENT_DIR/../joplin/manage.py loaddata $CURRENT_DIR/../joplin/db/system-generated/seeding.datadump.json

# Load test admin
pipenv run $CURRENT_DIR/../joplin/manage.py loaddata $CURRENT_DIR/../joplin/db/system-generated/local_admin_user.json
