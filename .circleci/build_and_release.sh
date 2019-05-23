#!/usr/bin/env bash
set -eo pipefail
CURRENT_DIR=`dirname $BASH_SOURCE`
source $CURRENT_DIR/helpers.sh
log() { log_base "build_and_release" $1 $2; }

joplin_print_header "Building Joplin Docker Image"

# Log in to dockerhub
docker login -u $DOCKER_USER -p $DOCKER_PASS

log "Building:"
log "Image Tags:        ${DOCKER_TAG_1}"
log "                   ${DOCKER_TAG_2}"
log "                   ${DOCKER_TAG_HEROKU}"
log "Branch:            ${CIRCLE_BRANCH}"
log "Application Name:  ${APPNAME}"

# DOCKER_BUILDKIT=1 allows us to specify a --target within our app.Dockerfile
# Adds 3 tags
# Builds using top-level directory ($CURRENT_DIR/..) as context
DOCKER_BUILDKIT=1 docker build -f app.Dockerfile -t $DOCKER_TAG_1 -t $DOCKER_TAG_2 -t $DOCKER_TAG_HEROKU --target $DOCKER_TARGET $CURRENT_DIR/..

# Push all 3 tags (2 to dockerhub, 1 to heroku)
docker push $DOCKER_TAG_1
docker push $DOCKER_TAG_2
docker push $DOCKER_TAG_HEROKU

joplin_print_header "Releasing Image"

# Release the container to heroku
heroku container:release web --app $APPNAME

joplin_print_header "Running Database Migration"

# Manually run entrypoint script
log "Migrating data for App: ${APPNAME}";
heroku run --app $APPNAME -- /app/docker-entrypoint.sh
