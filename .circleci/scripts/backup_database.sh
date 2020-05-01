#!/usr/bin/env bash
set -eo pipefail
CURRENT_DIR=`dirname $BASH_SOURCE`
source $CURRENT_DIR/helpers.sh
log() { log_base "backup_database" "$1" "$2"; }

# Check if APP/DB exists
APP_DB_EXISTS=$(app_database_attached $APPNAME)

if [ $APP_DB_EXISTS == "true" ]; then
  print_header "Creating Database Backup in S3"

  # Create a new backup
  heroku pg:backups:capture -a $APPNAME

  # Download the new backup
  LOCAL_DUMP_FILENAME=$APPNAME.dump
  heroku pg:backups:download -a $APPNAME -o $LOCAL_DUMP_FILENAME

  # upload to s3
  DB_CONNECTION_STRING=$(heroku config:get DATABASE_URL -a $APPNAME);
  LATEST_MIGRATION=$(psql $DB_CONNECTION_STRING -qtA -c 'select name from django_migrations order by id desc limit 1;')
  BACKUP_TIMESTAMP=$(date '+%Y-%m-%d--%H-%M-%S')
  S3_DUMP_FILENAME="${APPNAME}.${BACKUP_TIMESTAMP}.${SHA}.${LATEST_MIGRATION}.dump"
  S3_BUCKET_FILE_URL="s3://joplin-austin-gov-archive/deployment-backups/database/${APPNAME}/${S3_DUMP_FILENAME}"

  log 1 "Performing Database Backup for Branch: $1, App: $APPNAME."
  log 2 "App Name: ${APPNAME}."
  log 2 "Date Timestamp: ${BACKUP_TIMESTAMP}."
  log 2 "Latest Django Migration ID: ${LATEST_MIGRATION}."
  log 2 "S3 File URL: ${S3_BUCKET_FILE_URL}"
  log 2 "Beginning database backup process."

  aws s3 cp $LOCAL_DUMP_FILENAME $S3_BUCKET_FILE_URL
fi
