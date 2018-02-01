#!/usr/bin/env bash

set -o errexit

docker exec --interactive --tty joplin python joplin/manage.py dumpdata --indent 2 --natural-primary --natural-foreign --exclude sessions --exclude wagtailcore.grouppagepermission > fixtures/live.json
