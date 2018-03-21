#!/usr/bin/env bash
set -o errexit

echo "Running migrations..."
python ./joplin/manage.py migrate --noinput

if [ "x$LOAD_DATA" = 'xon' ]; then
  echo "Loading users..."
  python ./joplin/manage.py loaddata fixtures/users.json

  echo "Loading data..."
  python ./joplin/manage.py loadcontent \
        fixtures/images.yaml \
        fixtures/topics.yaml \
        fixtures/locations.yaml \
        fixtures/contacts.yaml \
        fixtures/departments.yaml \
        fixtures/services
fi

exec "$@"
