#!/usr/bin/env bash
set -o errexit

# run this file with: pipenv run bash .circleci/scripts/run_tests.sh
CURRENT_DIR=`dirname $BASH_SOURCE`
DEPLOYMENT_MODE="TEST"

PREV_DIR=$(pwd)
function clean_up {
  cd $PREV_DIR
}
trap clean_up EXIT
cd $CURRENT_DIR/../../joplin

echo "Running these test files:"
find . -name test_*.py
echo ""

# Skipped test files are prefixed with an underscore _
skipped_test_count=$(find . -name _test_*.py | wc -l)
if [ $skipped_test_count -gt 0 ]; then
  echo "You need to update these tests:"
  find . -name _test_*.py
  echo ""
fi

python manage.py test --pattern="test_*.py"
