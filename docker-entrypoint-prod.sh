#!/usr/bin/env bash
echo "Running migrations (Database & static files to S3 bucket) ..."
echo "Bucket: ${AWS_S3_BUCKET}"
echo "Bucket User: ${AWS_S3_USER}"
echo "Bucket ID: ${AWS_S3_KEYID}"...

python ./joplin/manage.py migrate --noinput
python ./joplin/manage.py collectstatic --noinput
