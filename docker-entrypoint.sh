#!/usr/bin/env bash
set -o errexit

echo "Running migrations..."
python ./joplin/manage.py migrate --noinput

./load-data.sh

if [ "x$WATCH_LOCAL" = 'xon' ]; then
  echo "Watching using the assets container. Skipping webpack step."
else
  echo "Building assets with webpack..."
  cd joplin
  yarn
  yarn build
  cd ..
fi

exec "$@"
