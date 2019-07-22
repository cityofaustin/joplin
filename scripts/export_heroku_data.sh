#!/usr/bin/env bash
set -o errexit
CURRENT_DIR=`dirname $BASH_SOURCE`

# Run this script within production heroku app to get production data for seeding.
# Replaces all user passwords with default admin test password.
# Executes user sanitation on production app itself so that no production passwords are ever on your local machine.
# Called by migration-test.sh
python ./joplin/manage.py dumpdata --indent 2 --natural-foreign --natural-primary -- | \
  jq '(.[] | select(.model == "users.user") | .fields.password) |= "pbkdf2_sha256$150000$GJQ1UoZlgrC4$Ir0Uww/i9f2VKzHznU4B1uaHbdCxRnZ69w12cIvxWP0="' \
