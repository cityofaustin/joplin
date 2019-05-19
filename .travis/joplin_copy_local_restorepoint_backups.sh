#!/usr/bin/env bash
CURRENT_DIR=`dirname $BASH_SOURCE`
source $CURRENT_DIR/heroku-helper.sh

#
# Copies the local database files (obtained from github) into the S3 for use in the migration process.
#
function joplin_copy_local_restorepoint_backups {

    # Validate Branch Name (or halt deployment if no branch specified)
    helper_internal_validation ${FUNCNAME[0]} $1

    # We're good to go!
    if [ "$?" = "0" ]; then
        joplin_print_header "Copying Database Files to Bucket"

        APPNAME=$(joplin_resolve_heroku_appname)
        S3_BUCKET_FILE_URL="s3://${AWS_S3_BUCKET_ARCHIVE_DEFAULT}/${AWS_S3_BUCKET_ARCHIVE_LOCATION_DEFAULT}/${APPNAME}"

        joplin_log ${FUNCNAME[0]} 0 "Current app:       '${APPNAME}'";
        joplin_log ${FUNCNAME[0]} 0 "Path Generated:    '${S3_BUCKET_FILE_URL}'";

        joplin_log ${FUNCNAME[0]} 0 "Copying files, please wait a few moments.'";
        aws s3 cp ./joplin/db/backups $S3_BUCKET_FILE_URL --recursive

        if [ "$?" != "0" ]; then
            helper_halt_deployment "There seems to have been a problem copying the files to the S3 bucket."
        fi;

        joplin_log ${FUNCNAME[0]} 0 "Process complete.";
  	fi;
}
