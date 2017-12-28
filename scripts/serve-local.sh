#!/usr/bin/env bash

set -o errexit

TAG='joplin:local'

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

docker build --tag "$TAG" .
docker run \
    --rm \
    --name joplin \
    --tty --interactive \
    --publish 8000:80 \
    --volume "$PWD:/app" \
    --env "LOAD_DATA=$LOAD_DATA" \
    "$TAG" "$@"
