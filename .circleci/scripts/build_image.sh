#!/usr/bin/env bash
set -eo pipefail
CURRENT_DIR=`dirname $BASH_SOURCE`
source $CURRENT_DIR/helpers.sh
log() { log_base "build" "$1" "$2"; }

print_header "Building Joplin Docker Image"

# Log in to dockerhub
docker login -u $DOCKER_USER -p $DOCKER_PASS

log 1 "Building:"
log 2 "Image Tags:        ${DOCKER_TAG_1}"
log 2 "                   ${DOCKER_TAG_2}"
log 2 "                   ${DOCKER_TAG_HEROKU}"
log 2 "Branch:            ${CIRCLE_BRANCH}"
log 2 "Application Name:  ${APPNAME}"

# DOCKER_BUILDKIT=1 allows us to specify a --target within our app.Dockerfile
# Adds 3 tags
# Builds using top-level directory ($CURRENT_DIR/..) as context
DOCKER_BUILDKIT=1 docker build -f app.Dockerfile -t $DOCKER_TAG_1 -t $DOCKER_TAG_2 -t $DOCKER_TAG_HEROKU --target $DOCKER_TARGET $CURRENT_DIR/../..

if [ "$CIRCLE_BRANCH" == "master" ] || [ "$CIRCLE_BRANCH" == "production" ] || [ "$CIRCLE_BRANCH" == "3396-dummy-data" ]; then
  # Push master and production images to dockerhub repo for storage
  print_header "Pushing Image to Dockerhub"
  docker push $DOCKER_TAG_1
  docker push $DOCKER_TAG_2
fi

print_header "Pushing Image to Heroku"
heroku container:login
docker push $DOCKER_TAG_HEROKU
