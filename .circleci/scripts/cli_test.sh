#!/usr/bin/env bash
set -e
CURRENT_DIR=`dirname $BASH_SOURCE`
source $CURRENT_DIR/helpers.sh

echo "Testing AWS CLI is installed"
aws --version

echo "Testing AWS has access to the buckets list"
aws s3api list-buckets --query "Buckets[].Name"

echo "Testing the Heroku CLI is installed"
heroku --version
