#!/usr/bin/env bash
set -e
CD=`dirname $BASH_SOURCE`
PREV_CD=$(pwd)

function clean_up {
  cd $PREV_CD
  if [ -f "$CD/zappa_settings.json" ]; then
    rm $CD/zappa_settings.json
  fi
}
trap clean_up EXIT

# sets .circleci/cleanup as your current directory
# necessary because "pipenv run zappa" wants zappa_settings to be at the "root" of your project directory.
cd $CD
pipenv run python ./build_zappa_settings.py

set +e
# Check if lambda function already exists.
# set +e temporarily allows us to throw errors.
# If `get-function` returns a 255 error, then we know that our lambda does not exist and needs to be deployed.
ZAPPA_FUNCTION=coa-joplin-build-cleanup-staging
$(aws lambda get-function --function-name $ZAPPA_FUNCTION > /dev/null)
result=$?
set -e
if [ "$result" == 0 ]; then
  # Update zappa lambda if it exists
  pipenv run zappa update staging
else
  # Deploy new lambda function if it doesn't exist
  pipenv run zappa deploy staging
fi
