#!/usr/bin/env bash
CURRENT_DIR=`dirname $BASH_SOURCE`
source $CURRENT_DIR/heroku-helper.sh

#
# Calls the release function for a specific image to a specific application
#
function joplin_release {

    # Validate Branch Name (or halt deployment if no branch specified)
    helper_internal_validation ${FUNCNAME[0]} $1

    # Not a test, and not an error
    if [ "$?" = "0" ]; then

        joplin_print_header "Releasing Image"

        # Retrieve App Name
        APPNAME=$(joplin_resolve_heroku_appname);

        # Determine image id to push
        DOCKER_IMAGE_ID=$(docker inspect registry.heroku.com/$APPNAME/web --format={{.Id}})

        if [ "$?" = "1" ]; then
            helper_halt_deployment "An error happened when trying to determine docker image id for '${APPNAME}'."
        fi;


        if [ "${DOCKER_IMAGE_ID}" = "" ]; then
            helper_halt_deployment "Could not determine image id to push for '${APPNAME}'."
        fi;

        joplin_log ${FUNCNAME[0]} 0 "Releasing Build for Branch: $TRAVIS_BRANCH, App: $APPNAME";
        joplin_log ${FUNCNAME[0]} 0 "Docker Image Id: $DOCKER_IMAGE_ID";

        # Gemerate json payload to upload via API
        JSON_PAYLOAD='{"updates":[{"type":"web","docker_image":"'"${DOCKER_IMAGE_ID}"'"}]}'

        # Make 'Release' API Call
        curl -n -X PATCH https://api.heroku.com/apps/$APPNAME/formation \
            -d "${JSON_PAYLOAD}" \
            -H "Content-Type: application/json" \
            -H "Accept: application/vnd.heroku+json; version=3.docker-releases" \
            -H "Authorization: Bearer ${HEROKU_API_KEY}"

        joplin_log ${FUNCNAME[0]} 0 "Release process finished";
    fi;
}
