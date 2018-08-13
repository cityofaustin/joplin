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
