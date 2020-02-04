#!/usr/bin/env bash
set -o errexit

# pipenv run sh .circleci/scripts/run_tests.sh
echo "What is BASH_SOURCE? [$BASH_SOURCE]"
echo "What is BASH_SOURCE[0]? [${BASH_SOURCE[0]}]"
echo "What is BASH_SOURCE[*]? [${BASH_SOURCE[*]}]"
CURRENT_DIR=`dirname $BASH_SOURCE`
python $CURRENT_DIR/../../joplin/manage.py test publish_preflight.tests.information_page_test
