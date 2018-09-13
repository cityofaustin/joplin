#!/usr/bin/env bash

#
# heroku_release - Calls the release function for a specific image to a specific application
#
# $1: The name of the application
# $2: The docker image id
#

function heroku_release() {

  B64AUTH=$(echo -n "_:$HEROKU_API_KEY" | base64)

  curl -n -X PATCH https://api.heroku.com/apps/$1/formation \
  -d '{ "updates": [{ "type": "web", "docker_image": "$2"}]}' \
  -H "Content-Type: application/json" \
  -H "Accept: application/vnd.heroku+json; version=3.docker-releases" \
  -H "Authorization: Basic ${B64AUTH}"
}


#
# heroku_release_token - Same as previous, uses OAuth method
#
# $1: The name of the application
# $2: The docker image id
#

function heroku_release_token() {
  curl -n -X PATCH https://api.heroku.com/apps/$1/formation \
  -d '{ "updates": [{ "type": "web", "docker_image": "$2"}]}' \
  -H "Content-Type: application/json" \
  -H "Accept: application/vnd.heroku+json; version=3.docker-releases" \
  -H "Authorization: Bearer ${HEROKU_API_KEY}"
}
