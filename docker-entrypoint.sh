#!/usr/bin/env bash
set -o errexit

./migrate-load-data.sh

exec "$@"
