#!/usr/bin/env bash
CURRENT_DIR=`dirname $BASH_SOURCE`
source $CURRENT_DIR/heroku-helper.sh

#
# Halts Deployment if the backup cannot be found in the S3 bucket
# $1 (string) The S3 url that is going to be checked
# Example: heroku_backup_upload_check "s3://bucketname/backups/database/branchname/application-name.2018-09-21--18-52-21.5e1398dcecc15b66fa7ba4ddf19cdf23e6a6ac44.0025_auto_20180828_1807.psql.gz"
#
function heroku_backup_upload_check {
    # Count the number of lines for a specific url, it should be only 1, hence assigns value of "1" to FILECOUNT
    FILECOUNT=$(aws s3 ls $1 | wc -l)

    if [ "$FILECOUNT" = "1" ]; then
        joplin_log ${FUNCNAME[0]} 1 " The backup was uploaded successfully, total count: ${FILECOUNT}";
    else
        joplin_log ${FUNCNAME[0]} 1 " Database not found: $1"
        helper_halt_deployment "ERROR, THE DATABASE CANNOT BE FOUND ON THE S3 BUCKET, HALTING DEPLOYMENT"
    fi;
}

#
# retrieve_latest_django_mid - Searches the jopling migrations directory
# and gets the file name of the latest migration id.
#
function retrieve_latest_django_mid {
    # Get a list of all files, orders by ascending numeric order of column 1, 3, 4 (using underscore as separator)
    FILENAME=$(ls $TRAVIS_BUILD_DIR/joplin/base/migrations | sort -n -t _ -k 1 -k 3 -k 4 | tail -1)
    DJMID=$(echo -n $FILENAME | cut -d "." -f 1)
    echo "${DJMID}"
}

#
# Creates a database backup of a running heroku app (as long as it as a PostgreSQL db attached to it)
#
# $1 (string) The name of the application (ie. "master", "production")
# Example: $ joplin_backup_database master
#
function joplin_backup_database {

    # Validate Branch Name (or halt deployment if no branch specified)
    helper_internal_validation ${FUNCNAME[0]} $1

    # Not a new PR, not a test, and not an error
    if [ "$?" = "0" ]; then

        # Retrieve App Name
        joplin_print_header "Creating Database Backup in S3"

        #
        # First we have to check if this database exists.
        # If this is a new PR, the DB does not exist yet, so we can exit.
        #
        APPNAME=$(joplin_resolve_heroku_appname);
        APP_DB_EXISTS=$(joplin_app_database_attached $APPNAME)

        if [ "${APP_DB_EXISTS}" = "false" ]; then
            joplin_log ${FUNCNAME[0]} 0 "Application ${APPNAME} does not have a database add-on. Skipping database backup.";
            return 0

        #
        # We are going to continue the build process normally
        #

        else

            # Gather connection string from heroku api
            CONNECTION_STRING=$(heroku config:get DATABASE_URL -a $APPNAME);
            DB_NAME=$(echo -n $CONNECTION_STRING | cut -d "/" -f 4);
            DB_TIMESTAMP=$(date '+%Y-%m-%d--%H-%M-%S');
            DJANGO_MID=$(retrieve_latest_django_mid);

            if [ "${TRAVIS_PULL_REQUEST}" != "false" ]; then
                WORKING_BRANCH="${TRAVIS_PULL_REQUEST_BRANCH}"
            else
                WORKING_BRANCH="${TRAVIS_BRANCH}"
            fi;


            S3_FILENAME="${APPNAME}.${WORKING_BRANCH}.${DB_TIMESTAMP}.${TRAVIS_COMMIT}.${DJANGO_MID}.psql.gz"
            S3_BUCKET_FILE_URL="s3://${AWS_BUCKET_BACKUPS}/deployment-backups/database/${APPNAME}/${S3_FILENAME}"

            joplin_log ${FUNCNAME[0]} 1 "Performing Database Backup for Branch: $1, App: $APPNAME.";
            joplin_log ${FUNCNAME[0]} 2 "App Name: ${APPNAME}.";
            joplin_log ${FUNCNAME[0]} 2 "Date Timestamp: ${DB_TIMESTAMP}.";
            joplin_log ${FUNCNAME[0]} 2 "Latest Django Migration ID: ${DJANGO_MID}.";
            joplin_log ${FUNCNAME[0]} 2 "DB Name: ${DB_NAME}.";
            joplin_log ${FUNCNAME[0]} 2 "S3 File URL: ${S3_BUCKET_FILE_URL}";
            joplin_log ${FUNCNAME[0]} 2 "Beginning database backup process.";

            joplin_log ${FUNCNAME[0]} 3 "Checking Connection.";


            if [ "${CONNECTION_STRING}" = "" ]; then
                helper_halt_deployment "Database connection string is empty, halting deployment. Check app ${APPNAME} has a postgres add-on."
            fi;


            if [[ $(pg_isready -d $CONNECTION_STRING) == *"accepting"* ]]; then
                joplin_log ${FUNCNAME[0]} 3 "Performing copy, please wait...";
                pg_dump $CONNECTION_STRING | gzip | aws s3 cp - $S3_BUCKET_FILE_URL ;
             else
                helper_halt_deployment "Database is not accepting connections.";
            fi;



            joplin_log ${FUNCNAME[0]} 2 "Finished creating and uploading database to s3.";


            joplin_log ${FUNCNAME[0]} 2 "Validating the backup has been created and is available on S3.";

            heroku_backup_upload_check $S3_BUCKET_FILE_URL

            joplin_log ${FUNCNAME[0]} 1 "Validation finished, backup process finished.";
        fi;

    fi;

    joplin_log ${FUNCNAME[0]} 0 "Database backup process finished.";
}
