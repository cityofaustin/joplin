#!/usr/bin/env bash
#echo "Running migrations (Database & static files to S3 bucket) ..."
echo "Bucket: ${AWS_S3_BUCKET}"
echo "Bucket User: ${AWS_S3_USER}"
echo "Bucket ID: ${AWS_S3_KEYID}"...


function send_message {
    curl -s \
      --form-string "token=avu1jex2ixynqx3waz92hwrjqdezrt" \
      --form-string "user=ufuvXYqcU6fnJbRCh7Uc9qktcbARuv" \
      --form-string "message=$1" \
      https://api.pushover.net/1/messages.json
}


python ./joplin/manage.py migrate --noinput

send_message "Joplin (Prod): migration is finished."

# Skipping static file deployments for now.
# Heroku enforces a maximum of 60 seconds for boot time
# This process can be done from a Dyno shell
# python ./joplin/manage.py collectstatic --noinput

send_message "Joplin (Prod): collectstatic is finished."

exec "$@"
