# pipenv run sh .circleci/scripts/run_tests.sh
CURRENT_DIR=`dirname $BASH_SOURCE`
python $CURRENT_DIR/../../joplin/manage.py test publish_preflight.tests.information_page_test
