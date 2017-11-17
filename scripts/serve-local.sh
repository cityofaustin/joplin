#!/usr/bin/env bash

set -o errexit

TAG='joplin:local'

docker build --tag "$TAG" .
docker run \
    --rm \
    --name joplin \
    --tty --interactive \
    --publish 8000:80 \
    --volume "$PWD:/app" \
    "$TAG" "$@"
