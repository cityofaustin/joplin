#!/usr/bin/env bash
echo "-- Entrypoint Executed (docker-entrypoint-prod.sh)"
echo "--    Bucket: ${AWS_S3_BUCKET}"
echo "--    Bucket User: ${AWS_S3_USER}"
echo "--    Bucket ID: ${AWS_S3_KEYID}"
exec "$@"
