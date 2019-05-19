#!/bin/bash
set -e
DEPLOY_ENV=$1
CURRENT_DIR=`dirname $BASH_SOURCE`

# Allows us to use BUILDKIT features like adding a --target to docker build
# Only works for "docker build" not "docker-compose ... --build"
export DOCKER_BUILDKIT=1

if [ $DEPLOY_ENV == "dev" ]; then
  $DOCKER_TARGET="dev"
  $DOCKER_TAG="joplin_app:dev"
elif [ $DEPLOY_ENV == "staging" ]; then
  $DOCKER_TARGET="staging"
  $DOCKER_TAG="joplin_app:staging"
elif [ $DEPLOY_ENV == "prod" ]; then
  $DOCKER_TARGET="prod"
  $DOCKER_TAG="joplin_app:prod"
fi

docker build -f Dockerfile.app -t $DOCKER_TAG --target $DOCKER_TARGET_APP $CURRENT_DIR/..
