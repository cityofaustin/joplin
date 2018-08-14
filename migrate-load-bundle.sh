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

if [ "x$LOCAL" = 'xon' ]; then
  echo "Watching using the assets container. Skipping webpack step."
else
  echo "Building assets with webpack..."
  cd joplin
  yarn
  yarn build
  cd ..
fi
