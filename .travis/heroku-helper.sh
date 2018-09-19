#!/usr/bin/env bash

#
# heroku_release - Calls the release function for a specific image to a specific application
#
# $1 (string) The name of the application (ie. "joplin-staging", "joplin-personal")
# Example: $ heroku_release joplin-personal
#

function heroku_release {

    if [ "$1" = "" ]; then
        echo "heroku_release(): App name required (ie: '$ heroku_release joplin-personal')"
        return 0
    fi;

    DOCKER_IMAGE_ID=$(docker inspect registry.heroku.com/$1/web --format={{.Id}})
    JSON_PAYLOAD='{"updates":[{"type":"web","docker_image":"'"${DOCKER_IMAGE_ID}"'"}]}'

    curl -n -X PATCH https://api.heroku.com/apps/$1/formation \
    -d "${JSON_PAYLOAD}" \
    -H "Content-Type: application/json" \
    -H "Accept: application/vnd.heroku+json; version=3.docker-releases" \
    -H "Authorization: Bearer ${HEROKU_API_KEY}"

}


#
# backup_psql - Creates a datanase backup of a running heroku app (as long as it as a PostgreSQL db attached to it)
#
# $1 (string) The name of the application (ie. "joplin-staging", "joplin-personal")
# Example: $ backup_sql joplin-personal
#

function backup_psql {
    if [ "$1" = "" ]; then
        echo "backup_psql(): App name required (ie: '$ backup_psql joplin-personal')"
        return 0;
    fi;

    CONNECTION_STRING=$(heroku config:get DATABASE_URL -a $1);
    DB_NAME=$(echo -n $CONNECTION_STRING | cut -d "/" -f 4);
    DB_TIMESTAMP=$(date '+%Y-%m-%d--%H-%M-%S');

    echo "----- Performing Database Backup";
    echo "-- Date Timestamp: ${DB_TIMESTAMP}";
    echo "-- DB Name: ${DB_NAME}";
    echo "-- Performing copy, please wait...";

    pg_dump $CONNECTION_STRING | gzip | aws s3 cp - s3://$AWS_BUCKET_BACKUPS/$TRAVIS_BRANCH/$1.$DB_TIMESTAMP.psql.gz;
    echo "----- Finished Performing Database Backup";
}


#
# helper_test - Tests the helper has been initialized properly and ready to run
# Runs the functions without parameters forcing error output.
#

function helper_test {
    echo "----- Heroku Helper Test Initialized;";

    echo "-- Testing 'heroku_release' is ready: ";
    heroku_release;

    echo "-- Testing 'backup_psql' is ready: ";
    backup_psql;

    echo "----- Heroku Helper Test finished.";
}
