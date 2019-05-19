#!/usr/bin/env bash
CURRENT_DIR=`dirname $BASH_SOURCE`
source $CURRENT_DIR/heroku-helper.sh

function joplin_remove_db_ownership {
    # Validate Branch Name (or halt deployment if no branch specified)
    helper_internal_validation ${FUNCNAME[0]} $1

    # We're good to go!
    if [ "$?" = "0" ]; then
        joplin_print_header "Removing DB Backup Ownership & Extension Lines"

        find $DB_BACKUPS_PATH -type f -exec sed -i "/\(OWNER TO\|COMMENT ON EXTENSION plpgsql\|CREATE EXTENSION IF NOT EXISTS plpgsql\|DROP EXTENSION plpgsql\)/d" {} \;
    fi;
}
