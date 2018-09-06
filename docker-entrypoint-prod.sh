#!/usr/bin/env bash
echo "Running migrations (Database & static files to S3 bucket) ..."
echo "Bucket: ${AWS_S3_BUCKET}"
echo "Bucket User: ${AWS_S3_USER}"
echo "Bucket ID: ${AWS_S3_KEYID}"...

python ./joplin/manage.py migrate --noinput

# Skipping static file deployments for now.
# Heroku enforces a maximum of 60 seconds for boot time
# python ./joplin/manage.py collectstatic --noinput
