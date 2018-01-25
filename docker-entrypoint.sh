#!/usr/bin/env sh
set -o errexit

echo "Running migrations..."
python ./joplin/manage.py migrate --noinput

if [ "x$LOAD_DATA" = 'xon' ]; then
  echo "Loading initial data..."
  python ./joplin/manage.py loaddata fixtures/live.json
fi

exec "$@"
