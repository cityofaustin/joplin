#!/usr/bin/env bash

set -o errexit

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

if [ "$REBUILD" == "on" ]; then
    docker build --no-cache -f Dockerfile.base -t joplin-base .
    docker-compose -f docker-compose.local.yml up --build
else
    docker build -f Dockerfile.base -t joplin-base .
    docker-compose -f docker-compose.local.yml up
fi
