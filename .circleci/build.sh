#!/usr/bin/env bash
set -e
CURRENT_DIR=`dirname $BASH_SOURCE`

source $CURRENT_DIR/helpers.sh

ENV=$(get_env)
SHA=${CIRCLE_SHA1:0:7}

if [ $ENV == "dev" ]; then
  DOCKER_TARGET="joplin-dev"
  DOCKER_TAG_1="cityofaustin/joplin_app:dev-${CIRCLE_BRANCH}-latest"
  DOCKER_TAG_2="cityofaustin/joplin_app:dev-${CIRCLE_BRANCH}-${SHA}"
elif [ $ENV == "staging" ]; then
  DOCKER_TARGET="joplin-staging"
  DOCKER_TAG_1="cityofaustin/joplin_app:master-latest"
  DOCKER_TAG_2="cityofaustin/joplin_app:master-${SHA}"
elif [ $ENV == "prod" ]; then
  DOCKER_TARGET="joplin-prod"
  DOCKER_TAG_1="cityofaustin/joplin_app:production-latest"
  DOCKER_TAG_2="cityofaustin/joplin_app:production-${SHA}"
fi

docker login -u $DOCKER_USER -p $DOCKER_PASS
DOCKER_BUILDKIT=1 docker build -f Dockerfile.app -t $DOCKER_TAG_1 --target $DOCKER_TARGET $CURRENT_DIR/..
docker tag $DOCKER_TAG_1 $DOCKER_TAG_2
docker push $DOCKER_TAG_1
docker push $DOCKER_TAG_2
