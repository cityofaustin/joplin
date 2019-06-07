#!/usr/bin/env bash
set -o errexit

docker run -it --entrypoint "./scripts/handle-migration-conflicts.sh" --volume "$PWD:/app" joplin-app:local
