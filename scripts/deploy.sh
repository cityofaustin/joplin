#!/usr/bin/env bash

set -o errexit

APP='joplin-staging'

CURRENT_CONFIG=$(heroku config --app "$APP")

if [[ $CURRENT_CONFIG != *"JANIS_URL"* ]]; then
    heroku config:set LOAD_DATA=on JANIS_URL=https://janis-staging.herokuapp.com --app "$APP"
fi

if [[ $CURRENT_CONFIG != *"STYLEGUIDE_URL"* ]]; then
    heroku config:set STYLEGUIDE_URL=https://cityofaustin.github.io/digital-services-style-guide --app "$APP"
fi

heroku container:push web --app "$APP"
