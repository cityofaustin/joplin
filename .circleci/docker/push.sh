#!/usr/bin/env bash
CD=`dirname $BASH_SOURCE`

#  Deploy an image to the cityofaustin Dockerhub repo.
#  Enter the name of a Dockerfile in this directory as a param.
#  Use the exact version of the Docker Image in future scripts.
#  ex:
#    sh push.sh joplin-base
#    sh push.sh joplin-ci-build
#    sh push.sh joplin-ci-deploy

FILE="$CD/$1.Dockerfile"
if [ ! -f $FILE ]; then
  echo "Error: $FILE not found"
  exit 1
fi

echo "Building new version of $1"
SHA=$(git rev-parse HEAD)
TAG="cityofaustin/$1:${SHA:0:7}"
docker build -f "$CD/$1.Dockerfile" -t $TAG $CD/..

echo "Pushing $TAG"
docker push $TAG

echo "Success!"
