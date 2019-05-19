#!/usr/bin/env bash
CURRENT_DIR=`dirname $BASH_SOURCE`
source $CURRENT_DIR/heroku-helper.sh

#
# This function will parse a commit message command, initially implemented to help test deployments
# in different pipelines without having to modify and commit code.
#
# It takes no arguments, it parses the current commit message:

# Syntax:
#       [joplin-devops command-1:value-1 command-2:value-2 command-n:value-n ...]
#
# Example:
#       This my commit message [joplin-devops new-appname:the-great-panda set-pipeline:my-heroku-pipeline-name-here]
#
function joplin_parse_commit_message {

    joplin_log ${FUNCNAME[0]} 0 "Parsing Commit Comments: ${TRAVIS_COMMIT_MESSAGE}";

    if [[ "$TRAVIS_COMMIT_MESSAGE" = *"[joplin-devops"* ]]; then
        # Extract the lines from brakets '[...]'
        DEVOPS_COMMAND=$(echo $TRAVIS_COMMIT_MESSAGE | awk -F'[][]' '{print $2}');

        # Split the command into an array separated by spaces
        DEVOPS_LINES=($(echo -n $DEVOPS_COMMAND | tr ' ' '\n'))

        # For each item in array (
        for ITEM in "${DEVOPS_LINES[@]:1}"; do
                # Get the command name part
                DEVOPS_COMMAND_ACTION=$(echo $ITEM | cut -d ":" -f 1);
                # Get the value part
                DEVOPS_COMMAND_ARGUMENTS=$(echo $ITEM | cut -d " " -f 2 | cut -d ":" -f 2);

                # Log values for CI Logs
                joplin_log ${FUNCNAME[0]} 1 "Parsing Item: ${ITEM}";
                joplin_log ${FUNCNAME[0]} 1 "DEVOPS_COMMAND_ACTION: ${DEVOPS_COMMAND_ACTION}";
                joplin_log ${FUNCNAME[0]} 1 "DEVOPS_COMMAND_ARGUMENTS: ${DEVOPS_COMMAND_ARGUMENTS}";

                # Switch case the command name
                case "$DEVOPS_COMMAND_ACTION" in
                    # Changes the default name of the pipeline to the one specified in the command.
                    set-pipeline)
                        PIPELINE_NAME=$DEVOPS_COMMAND_ARGUMENTS
                        joplin_log ${FUNCNAME[0]} 2 "Set pipeline to: ${PIPELINE_NAME}";
                    ;;

                    # Overrides the PR number to be bult
                    set-prnum)
                        PIPELINE_PULL_REQUEST=$DEVOPS_COMMAND_ARGUMENTS
                        joplin_log ${FUNCNAME[0]} 2 "Set pipeline PIPELINE_PULL_REQUEST to: ${PIPELINE_PULL_REQUEST}";
                    ;;

                    # Sets the database to be imported when build process runs, needs name of db in s3 bucket
                    import-db)
                        joplin_log ${FUNCNAME[0]} 2 "Set database import to: ${PIPELINE_IMPORTDB} (Not yet implemented)";
                    ;;

                    # Pulls database from PR app or staging (ignored if this is master)
                    pull-db)
                        joplin_log ${FUNCNAME[0]} 2 "Set database import to: ${DEVOPS_COMMAND_ARGUMENTS} (Not yet implemented)";
                    ;;

                    # Changes the default name of the application to deploy to.
                    new-appname)
                        PIPELINE_DEPLOYMENT_APP=$DEVOPS_COMMAND_ARGUMENTS
                        joplin_log ${FUNCNAME[0]} 2 "Set app name to: ${PIPELINE_DEPLOYMENT_APP}";
                    ;;

                    # Handler for unknown commands.
                    *)
                        joplin_log ${FUNCNAME[0]} 1 "Unknown Command : ${ITEM}";
                    ;;
                esac;
        done

        # The loop is finished and we no longer need to proceed.
        joplin_log ${FUNCNAME[0]} 1 "Done parsing command.";
    fi;

    # Function is finished.
    joplin_log ${FUNCNAME[0]} 0 "Parsing Commit Comments -- END";
}

function joplin_tag_application {
    HEROKU_NEW_APP_NAME=$1

    joplin_log ${FUNCNAME[0]} 1 "Tagging application: ${HEROKU_NEW_APP_NAME} ...";

    # Set Environment Variables
    # PR Review Apps do not get access to S3 Buckets, only if deployment mode is REVIEWS3
    heroku config:set   \
            DEPLOYMENT_MODE=REVIEW \
            APPLICATION_NAME=$HEROKU_NEW_APP_NAME \
            AWS_S3_USER=$AWS_S3_USER_DEFAULT \
            AWS_S3_KEYID=$AWS_ACCESS_KEY_ID \
            AWS_S3_ACCESSKEY=$AWS_SECRET_ACCESS_KEY \
            AWS_S3_BUCKET=$AWS_BUCKET_REVIEWAPPS \
            AWS_S3_BUCKET_ARCHIVE=$AWS_S3_BUCKET_ARCHIVE_DEFAULT \
            AWS_S3_BUCKET_ARCHIVE_LOCATION=$AWS_S3_BUCKET_ARCHIVE_LOCATION_DEFAULT \
            DEBUG=1 \
            HEROKU_JANIS_APP_NAME="janis-staging" \
            JANIS_URL="https://janis-staging.herokuapp.com" \
            STYLEGUIDE_URL="https://cityofaustin.github.io/digital-services-style-guide" \
            --app $HEROKU_NEW_APP_NAME;

    joplin_log ${FUNCNAME[0]} 1 "Tagging Done";

}

#
# Builds a new review application and attaches the app to a pipeline with (review) status.
# $1 (string) The name of the app to create.
# $2 (string) The name of the pipeline
#
function joplin_create_heroku_preview_app {
    # The new app name
    HEROKU_NEW_APP_NAME=$1

    joplin_log ${FUNCNAME[0]} 1 "Creating new app on heroku: ${HEROKU_NEW_APP_NAME}  and attaching to pipeline: ${PIPELINE_NAME}"

    # Create app with specified name
    heroku create $HEROKU_NEW_APP_NAME --team $PIPELINE_TEAM

    # Add postgresql to the new app.
    joplin_attach_heroku_database $HEROKU_NEW_APP_NAME

    # Set Environment Variables
    joplin_tag_application $HEROKU_NEW_APP_NAME

    # Couple New app to pipeline (assign review (PR) stage):
    heroku pipelines:add $PIPELINE_NAME --app $HEROKU_NEW_APP_NAME --stage review
}

#
# Creates a pull request application and puts it in the specified pipeline.
# Requires no input variables.
#
function joplin_create_pr_app {
    # Validate Branch Name (or halt deployment if no branch specified)
    helper_internal_validation ${FUNCNAME[0]} $1

    if [ "$?" = "0" ]; then
        #
        # First, parse commit message into environment variables.
        #
        joplin_parse_commit_message;

        # Build Header,
        joplin_print_header "Build PR Application"


        # We need a Pull request number that can be altered if necessary: PIPELINE_PULL_REQUEST
        # If empty, then copy the value from TRAVIS_PULL_REQUEST
        # If not empty, then we take PIPELINE_PULL_REQUEST over TRAVIS_PULL_REQUEST

        ## If empty, assume TRAVIS_PULL_REQUEST
        if [ "${PIPELINE_PULL_REQUEST}" = "" ]; then
            PIPELINE_PULL_REQUEST=$TRAVIS_PULL_REQUEST;

        ## else, we proceed with whatever value is in PIPELINE_PULL_REQUEST
        fi;

        joplin_log ${FUNCNAME[0]} 0 "Beginning PR app creation process (PIPELINE_PULL_REQUEST: ${PIPELINE_PULL_REQUEST})"

        # If this is not a PR request, then move on to a regular deployment.
        if [ "${PIPELINE_PULL_REQUEST}" = "false" ]; then
            # This is not a new pr branch
            joplin_log ${FUNCNAME[0]} 0 "This is not a new PR branch: (PIPELINE_PULL_REQUEST: ${PIPELINE_PULL_REQUEST}, TRAVIS_PULL_REQUEST: ${TRAVIS_PULL_REQUEST})."
            joplin_log ${FUNCNAME[0]} 0 "Moving on, nothing to do here."

        # Else, we need to create a new PR review app.
        else
            # We have a legitimate pull request, so print out some details for logging.
            joplin_log ${FUNCNAME[0]} 1 ">>> PR REQUEST"


            # If no name specified for the new app in the commit message command,
            # then generate a new name automatically.
            if [ "${PIPELINE_DEPLOYMENT_APP}" = "" ]; then
                PIPELINE_DEPLOYMENT_APP="joplin-staging-pr-${PIPELINE_PULL_REQUEST}"
            fi;

            # Show current values
            joplin_log ${FUNCNAME[0]} 1 ">>> Deployment details:"
            joplin_log ${FUNCNAME[0]} 1 "Deploying new app:         ${PIPELINE_DEPLOYMENT_APP}"
            joplin_log ${FUNCNAME[0]} 1 "Into Pipeline:             ${PIPELINE_NAME}"


            # We now must check if the current PR already exists.
            joplin_log ${FUNCNAME[0]} 1 "Checking if review app already exists";
            APP_EXISTS=$(joplin_app_exists $PIPELINE_DEPLOYMENT_APP)

            # If the review app exists, then check
            if [ "$APP_EXISTS" = "true" ]; then
                joplin_log ${FUNCNAME[0]} 2 "App ${PIPELINE_DEPLOYMENT_APP} already exists, tagging & checking if database exists.";

                joplin_tag_application $PIPELINE_DEPLOYMENT_APP;

                APP_DB_EXISTS=$(joplin_app_database_attached $PIPELINE_DEPLOYMENT_APP)

                if [ "${APP_DB_EXISTS}" = "false" ]; then
                    joplin_log ${FUNCNAME[0]} 3 "No database detected, attaching new database to ${PIPELINE_DEPLOYMENT_APP}.";

                    joplin_attach_heroku_database  $PIPELINE_DEPLOYMENT_APP

                    joplin_log ${FUNCNAME[0]} 3 "Done.";
                else

                    joplin_log ${FUNCNAME[0]} 2 "The database already exists.";

                fi;

            # Let's go ahead and build the new review app with the new name
            else
                joplin_log ${FUNCNAME[0]} 2 "Creating app ${PIPELINE_DEPLOYMENT_APP} one moment.";

                joplin_create_heroku_preview_app $PIPELINE_DEPLOYMENT_APP
            fi;

            joplin_log ${FUNCNAME[0]} 1 "Done Creating PR Review App"
        fi;

        joplin_log ${FUNCNAME[0]} 0 "Done Building App"
    fi;
}
