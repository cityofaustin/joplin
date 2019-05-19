#!/usr/bin/env bash
CURRENT_DIR=`dirname $BASH_SOURCE`

source $CURRENT_DIR/joplin_backup_database.sh
source $CURRENT_DIR/joplin_remove_db_ownership.sh
source $CURRENT_DIR/joplin_copy_local_restorepoint_backups
source $CURRENT_DIR/joplin_create_pr_app
source $CURRENT_DIR/joplin_build
source $CURRENT_DIR/joplin_release
source $CURRENT_DIR/joplin_migrate

#
# helper_test - Tests the helper has been initialized properly and ready to run
# Runs the functions without parameters forcing error output.
#
function helper_test {
    joplin_print_header "Heroku Helper Testing"

    joplin_log ${FUNCNAME[0]} 0 "Heroku Helper Test Initialized: ";
    joplin_log ${FUNCNAME[0]} 0 "Test tag: '${TRAVIS_CI_TEST_TAG}': ";

    joplin_log ${FUNCNAME[0]} 1 "Testing 'joplin_release' is ready: ";
    joplin_release $TRAVIS_CI_TEST_TAG;

    joplin_log ${FUNCNAME[0]} 1 "Testing 'joplin_release' is ready: ";
    joplin_backup_database $TRAVIS_CI_TEST_TAG;

    joplin_log ${FUNCNAME[0]} 1 "Testing 'joplin_reset_db_backups_owner' is ready: ";
    joplin_reset_db_backups_owner $TRAVIS_CI_TEST_TAG

    joplin_log ${FUNCNAME[0]} 1 "Testing 'joplin_remove_db_ownership' is ready: ";
    joplin_remove_db_ownership $TRAVIS_CI_TEST_TAG

    joplin_log ${FUNCNAME[0]} 1 "Testing 'joplin_copy_local_restorepoint_backups' is ready: ";
    joplin_copy_local_restorepoint_backups $TRAVIS_CI_TEST_TAG;

    joplin_log ${FUNCNAME[0]} 1 " Testing django migration id: ";
    retrieve_latest_django_mid;

    joplin_log ${FUNCNAME[0]} 1 "Testing 'joplin_build' is ready: ";
    joplin_build $TRAVIS_CI_TEST_TAG;

    joplin_log ${FUNCNAME[0]} 1 "Testing 'joplin_migrate' is ready: ";
    joplin_migrate $TRAVIS_CI_TEST_TAG;

    joplin_log ${FUNCNAME[0]} 1 "Testing 'joplin_create_pr_app' is ready: ";
    joplin_create_pr_app $TRAVIS_CI_TEST_TAG;

    joplin_log ${FUNCNAME[0]} 0 "Heroku Helper Test finished: ";
}
