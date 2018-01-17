#!/usr/bin/env bash

set -o errexit

TAG='joplin:local'

docker build --tag "$TAG" .
docker run \
    --rm \
    --name joplin-test \
    --tty --interactive \
    --volume "$PWD:/app" \
    "$TAG" python ./joplin/manage.py check
