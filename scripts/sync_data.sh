#!/usr/bin/env bash
set -o errexit

# Usage:
# bash scripts/sync_data.sh APP_SOURCE APP_DEST
# APP_SOURCE is the joplin app you want to extract data from.
# APP_DEST is the joplin app you want to send that data to.
# Use optional -d flag to sync documents too (skip if you aren't testing documents on your PR).
# bash scripts/sync_data.sh APP_SOURCE APP_DEST -d

APP_SOURCE=$1
APP_DEST=$2
GET_DOCUMENTS=$3

if [ "$APP_DEST" == "joplin" ]; then
  echo "No. Don't overwrite the production database."
  exit 1
fi

heroku pg:copy $APP_SOURCE::DATABASE_URL DATABASE_URL -a $APP_DEST

if [ "$GET_DOCUMENTS" == "-d" ]; then
  echo "Copying documents over."
  if [ "$APP_SOURCE" == "joplin" ]; then
    # Get Production documents location
    DOC_SOURCE="joplin3-austin-gov-static/production/media/documents"
  elif [ "$APP_SOURCE" == "joplin-staging" ]; then
    # Get Staging documents location
    DOC_SOURCE="joplin3-austin-gov-static/staging/media/documents"
  else
    # Get Review App documents location
    SOURCE_BRANCH=$(heroku config:get CIRCLE_BRANCH -a $APP_SOURCE)
    if [ -z "$SOURCE_BRANCH" ]; then
      echo "No CIRCLE_BRANCH found for $APP_SOURCE"
      exit 1
    fi
    DOC_SOURCE="joplin3-austin-gov-static/review/$SOURCE_BRANCH/media/documents"
  fi

  if [ "$APP_DEST" == "joplin-staging" ]; then
    # Get Staging documents location
    DOC_DEST="joplin3-austin-gov-static/staging/media/documents"
  else
    # Get Review App documents location
    DEST_BRANCH=$(heroku config:get CIRCLE_BRANCH -a $APP_DEST)
    if [ -z "$DEST_BRANCH" ]; then
      echo "No CIRCLE_BRANCH found for $APP_DEST"
      exit 1
    fi
    DOC_DEST="joplin3-austin-gov-static/review/$DEST_BRANCH/media/documents"
  fi

  aws s3 sync s3://$DOC_SOURCE s3://$DOC_DEST --only-show-errors --delete
fi
