#!/usr/bin/env bash
set -o errexit


# makes migrations, with merge flag to handle conflics
echo "making Schema Migrations"
python ./joplin/manage.py makemigrations --merge --noinput
