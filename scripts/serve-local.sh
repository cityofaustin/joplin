#!/usr/bin/env bash

set -o errexit

TAG='joplin:local'
ASSETSTAG='joplinassets:local'

DB_FILE='./joplin/db.sqlite3'
LOAD_DATA="$LOAD_DATA"
if [ -z "$LOAD_DATA" ] && [ ! -f "$DB_FILE" ]; then
    echo "DB file $DB_FILE not found, loading initial data"
    LOAD_DATA=on
fi

if [ "$LOAD_DATA" == "on" ] && [ -f "$DB_FILE" ]; then
    read -p "$DB_FILE exists. Do you want to delete it before loading data? [y/N] " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        echo "Deleting $DB_FILE at user request..."
        rm "$DB_FILE"
    fi
fi

# Get the heroku key. We eat stderr because the heroku cli will warn us that these tokens
# are short-lived. That's OK in our case because we're just running this locally.
HEROKU_KEY=$(heroku auth:token 2> /dev/null)

docker build --tag "$ASSETSTAG" --file Dockerfile.assets .
docker run --rm --detach --name joplinassets "$ASSETSTAG" yarn watch

docker build --tag "$TAG" .
docker run \
    --rm \
    --name joplin \
    --tty --interactive \
    --publish 8000:80 \
    --volume "$PWD:/app" \
    --env "DEBUG=1" \
    --env "LOAD_DATA=$LOAD_DATA" \
    --env "GUNICORN_CMD_ARGS=--reload  --reload-engine=poll" \
    --env "HEROKU_KEY=$HEROKU_KEY" \
    --env "HEROKU_JANIS_APP_NAME=$HEROKU_JANIS_APP_NAME" \
    --env "JANIS_URL=http://localhost:3000" \
    --env "STYLEGUIDE_URL=https://cityofaustin.github.io/digital-services-style-guide" \
    "$TAG" "$@"
