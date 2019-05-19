#!/usr/bin/env bash
CURRENT_DIR=`dirname $BASH_SOURCE`
source $CURRENT_DIR/heroku-helper.sh

#
# Runs a migration process in a heroku dyno on the target application
#
function joplin_migrate {
    # Validate Branch Name (or halt deployment if no branch specified)
    helper_internal_validation ${FUNCNAME[0]} $1

    # Not a test, and not an error
    if [ "$?" = "0" ]; then
        # Print a nice header
        joplin_print_header "Running Database Migration"

        # Retrieve App Name
        APPNAME=$(joplin_resolve_heroku_appname);

        echo -e "\n"
        joplin_log ${FUNCNAME[0]} 0 "Migrating data for Branch: ${TRAVIS_BRANCH}, App: ${APPNAME}";
        migration_output=`heroku run --app $APPNAME -- /app/migrate-load-data.sh`

        echo $migration_output;

        if [[ $migration_output == *"MIGRATION_EXIT_STATUS_ERROR"* ]]; then
            helper_halt_deployment "There has been an error in the migration process. Marking as a failed deployment.";
        fi;

        echo -e "\n"
        joplin_log ${FUNCNAME[0]} 0 "Migration process finished \n";
    fi;
}
