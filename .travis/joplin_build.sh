#!/usr/bin/env bash
CURRENT_DIR=`dirname $BASH_SOURCE`
source $CURRENT_DIR/heroku-helper.sh

#
# Builds the docker container and pushes the image to the heroku repository
# where it can be tagged to an app and released.
#
function joplin_build {

    # Validate Branch Name (or halt deployment if no branch specified)
    helper_internal_validation ${FUNCNAME[0]} $1

    # Not a test, and not an error
    if [ "$?" = "0" ]; then
        joplin_print_header "Building Joplin"

        # Retrieve App Name
        joplin_log ${FUNCNAME[0]} 0 "Resolving App Name for branch: $TRAVIS_BRANCH";
        APPNAME=$(joplin_resolve_heroku_appname $TRAVIS_BRANCH);
        joplin_log ${FUNCNAME[0]} 1 "App name resolved: ${APPNAME}";


        joplin_log ${FUNCNAME[0]} 1 "Logging in to Services ...";
        docker login --username=_ --password=$HEROKU_API_KEY registry.heroku.com

        joplin_log ${FUNCNAME[0]} 2 "Output Status: $?"

        if [ "$?" = "1" ]; then
            helper_halt_deployment "Could not log in to heroky registry for '${APPNAME}' "
        fi;

        joplin_log ${FUNCNAME[0]} 1 "Building:"
        joplin_log ${FUNCNAME[0]} 2 "Image Name:        ${JOPLIN_IMAGE_NAME}"
        joplin_log ${FUNCNAME[0]} 2 "Branch:            ${TRAVIS_BRANCH} (PR=${TRAVIS_PULL_REQUEST}, PRBRANCH=${TRAVIS_PULL_REQUEST_BRANCH})"
        joplin_log ${FUNCNAME[0]} 2 "Application Name:  ${APPNAME}"

        joplin_log ${FUNCNAME[0]} 2 "docker build -t $JOPLIN_IMAGE_NAME ."
        docker build -t $JOPLIN_IMAGE_NAME .

        joplin_log ${FUNCNAME[0]} 2 "Output Status: $?"

        if [ "$?" = "1" ]; then
            helper_halt_deployment "Could not build docker image for '${APPNAME}' "
        fi;

        joplin_log ${FUNCNAME[0]} 1 "Tagging Image"
        joplin_log ${FUNCNAME[0]} 1 "docker tag $JOPLIN_IMAGE_NAME registry.heroku.com/$APPNAME/web"
        docker tag $JOPLIN_IMAGE_NAME registry.heroku.com/$APPNAME/web

        joplin_log ${FUNCNAME[0]} 2 "Output Status: $?"

        if [ "$?" = "1" ]; then
            helper_halt_deployment "Could not tag docker image for '${APPNAME}' "
        fi;

        joplin_log ${FUNCNAME[0]} 1 "Pushing to Heroku Repository"
        joplin_log ${FUNCNAME[0]} 1 "docker push registry.heroku.com/$APPNAME/web"
        docker push registry.heroku.com/$APPNAME/web

        joplin_log ${FUNCNAME[0]} 2 "Output Status: $?"

        if [ "$?" = "1" ]; then
            helper_halt_deployment "Could not push docker image to Heroku registry for '${APPNAME}'."
        fi;



        joplin_log ${FUNCNAME[0]} 0 "Finished Building Container";
    fi;
}
