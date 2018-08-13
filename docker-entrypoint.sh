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
        fixtures/311.yaml \
        fixtures/themes.yaml \
        fixtures/topics.yaml \
        fixtures/locations.yaml \
        fixtures/contacts.yaml \
        fixtures/departments.yaml \
        fixtures/services \
        fixtures/processes
fi

if [ "x$WATCH_LOCAL" = 'xon' ]; then
  echo "Watching using the assets container. Skipping webpack step."
else
  echo "Building assets with webpack..."
  apt-get update
  apt-get -y install gnupg
  apt-get -y install curl
  curl -sL https://deb.nodesource.com/setup_10.x | bash -
  apt-get update
  apt-get -y install nodejs
  npm install --global yarn
  cd joplin
  yarn
  yarn build
  cd ..
fi

exec "$@"
