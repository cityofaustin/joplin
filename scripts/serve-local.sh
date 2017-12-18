#!/usr/bin/env bash

set -o errexit

TAG='joplin:local'

DB_FILE='./joplin/db.sqlite3'
LOAD_DATA="$LOAD_DATA"
if [ -z "$LOAD_DATA" ] && [ ! -f ./joplin/db.sqlite3 ]; then
    echo "DB file $DB_FILE not found, loading initial data"
    LOAD_DATA=on
fi

docker build --tag "$TAG" .
docker run \
    --rm \
    --name joplin \
    --tty --interactive \
    --publish 8000:80 \
    --volume "$PWD:/app" \
    --env "LOAD_DATA=$LOAD_DATA" \
    "$TAG" "$@"
