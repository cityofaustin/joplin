#!/usr/bin/env sh
set -o errexit

echo "Running migrations..."
python ./joplin/manage.py migrate --noinput

if [ "x$LOAD_DATA" = 'xon' ]; then
  echo "Loading initial data..."
  python ./joplin/manage.py loaddata fixtures/base.json fixtures/users.json fixtures/applicationblocks.json fixtures/pages.json
fi

exec "$@"
