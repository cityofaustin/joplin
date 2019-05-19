#!/usr/bin/env bash
set -e
CURRENT_DIR=`dirname $BASH_SOURCE`

source $CURRENT_DIR/helpers.sh

# Allows us to use BUILDKIT features like adding a --target to docker build
# Only works for "docker build" not "docker-compose ... --build"
export DOCKER_BUILDKIT=1

ENV=$(get_env)

if [ $ENV == "dev" ]; then
  $DOCKER_TARGET="dev"
  $DOCKER_TAG="joplin_app:dev"
elif [ $ENV == "staging" ]; then
  $DOCKER_TARGET="staging"
  $DOCKER_TAG="joplin_app:staging"
elif [ $ENV == "prod" ]; then
  $DOCKER_TARGET="prod"
  $DOCKER_TAG="joplin_app:prod"
fi

docker build -f Dockerfile.app -t $DOCKER_TAG --target $DOCKER_TARGET $CURRENT_DIR/..
