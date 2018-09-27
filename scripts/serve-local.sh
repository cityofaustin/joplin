#!/usr/bin/env bash

set -o errexit

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
