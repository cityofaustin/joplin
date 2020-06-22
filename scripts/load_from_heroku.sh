#!/usr/bin/env bash
set -o errexit
CURRENT_DIR=`dirname $BASH_SOURCE`
export TMP_DATADUMP=$CURRENT_DIR/../joplin/db/system-generated/tmp.datadump.json

APPNAME=$1

# Replace all user passwords with default admin test password
heroku run -xa $APPNAME python ./joplin/manage.py dumpdata --exclude=wagtailcore.GroupCollectionPermission --indent 2 --natural-foreign --natural-primary -- | \
  python ./scripts/remove_logs_from_json_stream.py | \
  jq '(.[] | select(.model == "users.user") | .fields.password) |= "pbkdf2_sha256$150000$GJQ1UoZlgrC4$Ir0Uww/i9f2VKzHznU4B1uaHbdCxRnZ69w12cIvxWP0="' \
  > $TMP_DATADUMP

# Note: this will only work if your local Joplin's migrations match production's.
#
# This command will drop your existing database.
# You only need to run this command once to load data. Once your data is loaded,
# you can run a normal `sh scripts/undockered.sh` with your pre-loaded data.
# If you're loading older data, make sure you check the changelog to ensure that your
# Joplin is compatible with your datadump.
UNDOCK=on DROP_DB=on LOAD_DATA=new_datadump sh $CURRENT_DIR/serve-local.sh
