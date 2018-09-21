#!/usr/bin/env bash


TRAVIS_CI_TEST_TAG="travis-ci-internal-test"

#
# Prints error message and stops deployment by returing exit 1
# $1 (string) - Error message to display
# Example: helper_halt_deployment "File not found"
#

function helper_halt_deployment {
    echo "$1" && exit 1;
}

#
# Helps validate branch name (or stops deployment if no branch specified)
# $1 (string) The name of the function callling this method
# $2 (string) the name of the branch
# Example: helper_internal_validation "heroku_test" "production"
#

function helper_internal_validation {
    # Show message if this is an internal test
    if [ "$2" = "${TRAVIS_CI_TEST_TAG}" ]; then
        echo "  > $1(): Ready to execute.";
        return 1
    fi;

    # Output error if no branch is specified.
    if [ "$2" = "" ]; then
        helper_halt_deployment "$1(): Branch name required (ie: '$1 staging'). Halting deployment."
    fi;

    return 0
}

#
# Turn the branch name into the app name in Heroku
# $1 (string) The name of the branch (ie. "master", "production", "pr-160")
#

function heroku_resolve_appname {

    # Turn the branch name into the application name we need
    # production:   joplin
    # master:       joplin-staging
    # sergiotest:   joplin-personal
    # anyother:     anyother

    case $1 in
        production)
            APPNAME="joplin"
            ;;
        master)
            APPNAME="joplin-staging"
            ;;
        sergiotest)
            APPNAME="joplin-personal"
            ;;
        *)
            APPNAME=$1
            ;;
    esac

    # Output results for logging
    echo "${APPNAME}"
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
# Halts Deployment if the backup cannot be found in the S3 bucket
# $1 (string) The S3 url that is going to be checked
# Example: heroku_backup_upload_check "s3://bucketname/backups/database/branchname/application-name.2018-09-21--18-52-21.5e1398dcecc15b66fa7ba4ddf19cdf23e6a6ac44.0025_auto_20180828_1807.psql.gz"
#

function heroku_backup_upload_check {
    # Count the number of lines for a specific url, it should be only 1, hence assigns value of "1" to FILECOUNT
    FILECOUNT=$(aws s3 ls $1 | wc -l)

    if [ "$FILECOUNT" = "1" ]; then
        echo "heroku_backup_upload_check() ----- The backup was uploaded successfully.";
    else
        echo "heroku_backup_upload_check() ----- ERROR, THE DATABASE CANNOT BE FOUND ON THE S3 BUCKET"
        echo "S3 URL: $1";
        # exit 1
    fi;
}

#
# Creates a database backup of a running heroku app (as long as it as a PostgreSQL db attached to it)
#
# $1 (string) The name of the application (ie. "master", "production")
# Example: $ backup_sql master
#

function heroku_backup_database {

    # Validate Branch Name (or halt deployment if no branch specified)
    helper_internal_validation ${FUNCNAME[0]} $1

    # Not a test, and not an error
    if [ "$?" = "0" ]; then
        # Retrieve App Name
        APPNAME=$(heroku_resolve_appname $1);

        # Gather connection string from heroku api
        CONNECTION_STRING=$(heroku config:get DATABASE_URL -a $APPNAME);
        DB_NAME=$(echo -n $CONNECTION_STRING | cut -d "/" -f 4);
        DB_TIMESTAMP=$(date '+%Y-%m-%d--%H-%M-%S');
        DJANGO_MID=$(retrieve_latest_django_mid);

        S3_BUCKET_FILE_URL="s3://${AWS_BUCKET_BACKUPS}/backups/database/${TRAVIS_BRANCH}/${APPNAME}.${DB_TIMESTAMP}.${TRAVIS_COMMIT}.${DJANGO_MID}.psql.gz"

        echo "heroku_backup_database() ----- Performing Database Backup for Branch: $1, App: $APPNAME";
        echo "heroku_backup_database() -- App Name: ${APPNAME}";
        echo "heroku_backup_database() -- Date Timestamp: ${DB_TIMESTAMP}";
        echo "heroku_backup_database() -- Latest Django Migration ID: ${DJANGO_MID}";
        echo "heroku_backup_database() -- DB Name: ${DB_NAME}";
        echo "heroku_backup_database() -- S3 File URL: ${S3_BUCKET_FILE_URL}";
        echo "heroku_backup_database() -- Performing copy, please wait...";

        pg_dump $CONNECTION_STRING | gzip | aws s3 cp - $S3_BUCKET_FILE_URL;
        echo "heroku_backup_database()----- Finished creating and uploading database to s3";

        echo "heroku_backup_database()----- Validating the backup has been created and is available on S3";
        heroku_backup_upload_check $S3_BUCKET_FILE_URL
        echo "heroku_backup_database()----- Validation finished, backup process finished.";
    fi;
}



#
# Creates a database backup of a running heroku app (as long as it as a PostgreSQL db attached to it)
#
# $1 (string) The name of the branch (ie. "master", "production")
# Example: $ backup_sql master
#

function heroku_build {

    # Validate Branch Name (or halt deployment if no branch specified)
    helper_internal_validation ${FUNCNAME[0]} $1

    # Not a test, and not an error
    if [ "$?" = "0" ]; then
        # Retrieve App Name
        APPNAME=$(heroku_resolve_appname $1);

        # Gather connection string from heroku api
        CONNECTION_STRING=$(heroku config:get DATABASE_URL -a $APPNAME);
        DB_NAME=$(echo -n $CONNECTION_STRING | cut -d "/" -f 4);
        DB_TIMESTAMP=$(date '+%Y-%m-%d--%H-%M-%S');

        echo "heroku_build() ----- Building Docker Container";
        echo "heroku_build() -- Logging in to Services";
        docker login --username=_ --password=$HEROKU_API_KEY registry.heroku.com
        echo "heroku_build() -- Building: '${JOPLIN_IMAGE_NAME}' for Branch: $1, App: $APPNAME";
        docker build -t $JOPLIN_IMAGE_NAME .
        echo "heroku_build() -- Tagging Image";
        docker tag $JOPLIN_IMAGE_NAME registry.heroku.com/$APPNAME/web
        echo "heroku_build() -- Pushing to Heroku Repository";
        docker push registry.heroku.com/$APPNAME/web
        echo "heroku_build()----- Finished Building Container";
    fi;
}


#
# Calls the release function for a specific image to a specific application
# $1 (string) The name of the branch (ie. "master", "production", "pr-160")
# Example: $ heroku_release master
#

function heroku_release {

    # Validate Branch Name (or halt deployment if no branch specified)
    helper_internal_validation ${FUNCNAME[0]} $1

    # Not a test, and not an error
    if [ "$?" = "0" ]; then
        # Retrieve App Name
        APPNAME=$(heroku_resolve_appname $1);

        # Determine image id to push
        DOCKER_IMAGE_ID=$(docker inspect registry.heroku.com/$APPNAME/web --format={{.Id}})

        echo "heroku_release() ----- Releasing Build for Branch: $1, App: $APPNAME";
        echo "heroku_release() ----- Docker Image Id: $DOCKER_IMAGE_ID";

        # Gemerate json payload to upload via API
        JSON_PAYLOAD='{"updates":[{"type":"web","docker_image":"'"${DOCKER_IMAGE_ID}"'"}]}'

        # Make 'Release' API Call
        curl -n -X PATCH https://api.heroku.com/apps/$APPNAME/formation \
        -d "${JSON_PAYLOAD}" \
        -H "Content-Type: application/json" \
        -H "Accept: application/vnd.heroku+json; version=3.docker-releases" \
        -H "Authorization: Bearer ${HEROKU_API_KEY}"
    fi;

}


#
# Runs a migration process in a heroku dyno on the target application
# $1 (string) The name of the branch (ie. "master", "production", "pr-160")
# Example: $ heroku_migrate staging
#

function heroku_migrate {

    # Validate Branch Name (or halt deployment if no branch specified)
    helper_internal_validation ${FUNCNAME[0]} $1

    # Not a test, and not an error
    if [ "$?" = "0" ]; then
        # Retrieve App Name
        APPNAME=$(heroku_resolve_appname $1);

        echo "heroku_migrate() ----- Migrating data for Branch: $1, App: $APPNAME";
        heroku run -a $APPNAME -- /app/migrate-load-data.sh
        echo "heroku_migrate() ----- Migration process finished.";
    fi;
}


#
# helper_test - Tests the helper has been initialized properly and ready to run
# Runs the functions without parameters forcing error output.
#

function helper_test {
    echo "helper_test() ----- Heroku Helper Test Initialized"
    echo "helper_test() ----- Test tag: ${TRAVIS_CI_TEST_TAG}";

    echo "helper_test() ----- Testing 'heroku_release' is ready: ";
    heroku_release $TRAVIS_CI_TEST_TAG;

    echo "helper_test() ----- Testing 'heroku_backup_database' is ready: ";
    heroku_backup_database $TRAVIS_CI_TEST_TAG;

    echo "helper_test() ----- Testing django migration id: ";
    retrieve_latest_django_mid;

    echo "helper_test() ----- Testing 'heroku_build' is ready: ";
    heroku_build $TRAVIS_CI_TEST_TAG;

    echo "heroku_migrate() ----- Testing 'heroku_migrate' is ready: ";
    heroku_migrate $TRAVIS_CI_TEST_TAG;

    echo "helper_test() ----- Heroku Helper Test finished.";
}

