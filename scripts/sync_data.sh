#!/usr/bin/env bash
set -o errexit

# Note: this script will overwrite all data in the destination app APP_DEST

# Usage:
# bash scripts/sync_data.sh APP_SOURCE APP_DEST
# APP_SOURCE is the joplin app you want to extract data from.
# APP_DEST is the joplin app you want to send that data to.

# OPTION is for syncing data beyond just the postgres database.
#   This param is optional. You can use 2 possible values with it.
#   -d will sync documents (skip if you aren't testing documents on your PR).
#   -m will sync the entire media folder (skip if images aren't important to your PR)
#   ex: sh scripts/sync_data.sh APP_SOURCE APP_DEST -m

APP_SOURCE=$1
APP_DEST=$2
OPTION=$3

if [ "$APP_DEST" == "joplin" ]; then
  echo "No. Don't overwrite the production database."
  exit 1
fi

heroku pg:copy $APP_SOURCE::DATABASE_URL DATABASE_URL -a $APP_DEST

if [ "$OPTION" == "-d" ] || [ "$OPTION" == "-m" ]; then
  if [ "$OPTION" == "-m" ]; then
    SUFFIX='media'
    echo "Copying media over."
  elif [ "$OPTION" == "-d" ]; then
    SUFFIX='media/documents'
    echo "Copying documents over."
  fi
  if [ "$APP_SOURCE" == "joplin" ]; then
    # Get Production documents location
    DOC_SOURCE="joplin3-austin-gov-static/production/$SUFFIX"
  elif [ "$APP_SOURCE" == "joplin-staging" ]; then
    # Get Staging documents location
    DOC_SOURCE="joplin3-austin-gov-static/staging/$SUFFIX"
  else
    # Get Review App documents location
    SOURCE_BRANCH=$(heroku config:get CIRCLE_BRANCH -a $APP_SOURCE)
    if [ -z "$SOURCE_BRANCH" ]; then
      echo "No CIRCLE_BRANCH found for $APP_SOURCE"
      exit 1
    fi
    DOC_SOURCE="joplin3-austin-gov-static/review/$SOURCE_BRANCH/$SUFFIX"
  fi

  if [ "$APP_DEST" == "joplin-staging" ]; then
    # Get Staging documents location
    DOC_DEST="joplin3-austin-gov-static/staging/$SUFFIX"
  else
    # Get Review App documents location
    DEST_BRANCH=$(heroku config:get CIRCLE_BRANCH -a $APP_DEST)
    if [ -z "$DEST_BRANCH" ]; then
      echo "No CIRCLE_BRANCH found for $APP_DEST"
      exit 1
    fi
    DOC_DEST="joplin3-austin-gov-static/review/$DEST_BRANCH/$SUFFIX"
  fi

  aws s3 sync s3://$DOC_SOURCE s3://$DOC_DEST --only-show-errors --delete
fi
