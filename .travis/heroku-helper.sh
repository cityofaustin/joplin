#!/usr/bin/env bash

# Tag used for testing
TRAVIS_CI_TEST_TAG="travis-ci-internal-test"

#
# Pipeline Variables
# These determine the exact pipeline in the heroku account where new PR (review apps) are created.
# It also determines which "team" group will be used.
#

# The team name (a sort of sub-account in heroku)
PIPELINE_TEAM=$PIPELINE_TEAM_DEFAULT
# The name of the pipeline in the team account.
PIPELINE_NAME=$PIPELINE_NAME_DEFAULT
# Pull Request holds the PR number, initially it remains empty, copies from TRAVIS and gets modified.
PIPELINE_PULL_REQUEST=""
# Deployment app is our target application
PIPELINE_DEPLOYMENT_APP=""



#
# Simply builds a noticeable header when parsing logs.
# This should help determine when our commands begin execution,
# and what branch is being affected by current deployment.
#

function joplin_build_header {
    echo ""
    echo ""
    echo "--------------------------------------------------------------"
    echo "   $1"
    echo "--------------------------------------------------------------"
    echo "  TRAVIS_BRANCH:          ${TRAVIS_BRANCH}"
    echo "  TRAVIS_PULL_REQUEST:    ${TRAVIS_PULL_REQUEST}"
    echo "  PIPELINE_TEAM:          ${PIPELINE_TEAM}"
    echo "  PIPELINE_NAME:          ${PIPELINE_NAME}"
    echo ""
}




#
# Prints an indention based on the calling function
# $1 (string) name of the function
# $2 (int) level
# $3 (string) text
# Example: joplin_log "myfunc" 3 "My Message";
# Example: joplin_log ${FUNCNAME[0]} 1 "My Message";
#       ${FUNCNAME[0]} holds the name of the function where it is being accessed from.
#

function joplin_log {
    RANGE=$(awk "BEGIN { print 5*${2} }")
    echo -n "${1}() "
    awk -v ORS=  "BEGIN { for (i = 1; i <= ${RANGE}; ++i) print \"-\" }" # leave ORS empty please
    echo " ${3}"
}


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



#
# Resolves the PR number for a branch.
# Requires no arguments, gets them from Travis environment.
#

#function joplin_branch_to_prnumber_deprecated {
#    # Gathers the initial branch id
#    BRANCH_ID=$(git rev-parse $TRAVIS_BRANCH)
#    # Now we cross-match the BRANCH ID with PR History
#    BRANCH_PR_DATA=$(git ls-remote origin 'pull/*/head' | grep $BRANCH_ID)
#    # Extract the PR Number from data
#    BRANCH_PR_NUMBER=$(echo -n $BRANCH_PR_DATA | cut -d '/' -f 3)
#    # Output Result
#    echo $BRANCH_PR_NUMBER;
#}


#
# Get PR Number for a specific branch in Joplin, using GitHub's API. (Rrequires curl and jq to be installed)
# curl -X GET -s https://api.github.com/repos/cityofaustin/joplin/pulls | jq -r '.[] | "\(.head.ref):\(.number)"'
# Requires no arguments, gets the branch number from Travis' environment.
#

function joplin_branch_to_prnumber {
	BRANCH_NAME=$TRAVIS_BRANCH
	if [ "${BRANCH_NAME}" = "" ]; then
	    echo "";
    else
        PR_NUMBER=$(curl -X GET -s https://api.github.com/repos/cityofaustin/joplin/pulls | jq -r '.[] | "\(.head.ref):\(.number)"' | grep "${BRANCH_NAME}" | cut -d ":" -f 2)
        echo "${PR_NUMBER}"
	fi;
}


#
# Returns the PR number, first it tries from the TRAVIS_PULL_REQUEST variable
# if that fails, then it tries to resolve it from the GitHub branch history.
#

function joplin_get_env_prnum {
    # If Travis CI does not have a pull request number, then resolve it.
    if [ "${TRAVIS_PULL_REQUEST}" = "false" ]; then
        PRNUM=$(joplin_branch_to_prnumber $TRAVIS_BRANCH);
        echo "${PRNUM}";
    # If we do have it, then use that instead (faster)
    else
        echo "${TRAVIS_PULL_REQUEST}";
    fi;
}


#
# Generates the app name for an app based on a nomenclature and PR number
# if a PR number is not given, then it will try to resolve it using the branch name
# $1 (int, string) The PR Number
#

function joplin_generate_app_name {

    # Get PR Number, if none given, then resolve.
    if [ "$1" = "" ]; then
        BRANCH_PR_NUMBER=$(joplin_branch_to_prnumber $TRAVIS_BRANCH)
     else
        BRANCH_PR_NUMBER=$1
    fi;

    echo "joplin-staging-pr-${BRANCH_PR_NUMBER}"
}



#
# Returns "True" if a given app name exists in heroku.
# $1 (string) The name of the app (ie. joplin-staging, joplin-pr-160)
#

function joplin_app_exists {

    HEROKU_TEAM_APPS=$(heroku apps --team $PIPELINE_TEAM | grep $1)

    if [ "${HEROKU_TEAM_APPS}" != "" ]; then
        echo "true";
    else
        echo "false"
    fi;
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
    #heroku create $NEW_APP_NAME

    # Add postgresql to the new app.
    #heroku addons:create heroku-postgresql:hobby-dev --version=9.6 --app $HEROKU_NEW_APP_NAME

    # Set Environment Variables
    # PR Review Apps do not get access to S3 Buckets
    #heroku config:set   DEPLOYMENT_MODE=REVIEW  --app $HEROKU_NEW_APP_NAME;

    # Couple New app to pipeline (assign review (PR) stage):
    #heroku pipelines:add $PIPELINE_NAME --app $HEROKU_NEW_APP_NAME --stage review
}





#
# Creates a pull request application and puts it in the specified pipeline.
# Requires no input variables.
#

function joplin_create_pr_app {

    # Validate Branch Name (or halt deployment if no branch specified)
    helper_internal_validation ${FUNCNAME[0]} $1

    #if [ "$?" = "0" ]; then
        # We should stop right here!
    #    exit 1;

        # Build Header,
        joplin_build_header "Build PR Application"

        #
        # First, parse commit message into environment variables.
        #
        joplin_parse_commit_message;

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
            joplin_log ${FUNCNAME[0]} 1 ">>> NEW PR REQUEST"
            joplin_log ${FUNCNAME[0]} 1 "PIPELINE_PULL_REQUEST: ${PIPELINE_PULL_REQUEST}"
            joplin_log ${FUNCNAME[0]} 1 "TRAVIS_PULL_REQUEST:   ${TRAVIS_PULL_REQUEST}"

            # Resolve GIT PR Number (for logging), and print.
            GIT_PR_NUM=$(joplin_branch_to_prnumber $TRAVIS_BRANCH)
            joplin_log ${FUNCNAME[0]} 1 "GIT PULL REQUEST NUM:  ${GIT_PR_NUM}"

            # If no name specified for the new app in the commit message command,
            # then generate a new name automatically.
            if [ "${PIPELINE_DEPLOYMENT_APP}" = "" ]; then
                PIPELINE_DEPLOYMENT_APP=$(joplin_generate_app_name $PIPELINE_PULL_REQUEST)
            fi;

            # Show current values
            joplin_log ${FUNCNAME[0]} 1 ">>> Deployment details:"
            joplin_log ${FUNCNAME[0]} 1 "Deploying new app:         ${PIPELINE_DEPLOYMENT_APP}"
            joplin_log ${FUNCNAME[0]} 1 "Into Pipeline:             ${PIPELINE_NAME}"


            # We now must check if the current PR already exists.
            joplin_log ${FUNCNAME[0]} 1 "Checking if review app already exists";
            APP_EXISTS=$(joplin_app_exists $PIPELINE_DEPLOYMENT_APP)

            # If the review app exists, we have to skip deployment
            if [ "$APP_EXISTS" = "true" ]; then
                joplin_log ${FUNCNAME[0]} 2 "App ${PIPELINE_DEPLOYMENT_APP} already exists, skipping deployment.";


            # Let's go ahead and build the new review app with the new name
            else
                joplin_log ${FUNCNAME[0]} 2 "Creating app ${PIPELINE_DEPLOYMENT_APP} one moment.";

                joplin_create_heroku_preview_app $PIPELINE_DEPLOYMENT_APP
            fi;

            joplin_log ${FUNCNAME[0]} 1 "Done Creating PR Review App"
        fi;

        joplin_log ${FUNCNAME[0]} 0 "Done Building App"
    #fi;
}




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
        helper_halt_deployment "$1(): Branch name required (ie: '$1 staging'). Halting deployment.";
    fi;


    joplin_log ${FUNCNAME[0]} 1 "We have a working branch: $2";
    return 0
}

#
# Turn the branch name into the app name in Heroku
# $1 (string) The name of the branch (ie. "master", "production", "pr-160")
#

function joplin_resolve_heroku_appname {

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
        *)
            APPNAME=$(joplin_generate_app_name)
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
        exit 1
    fi;
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


    # First check if this is a brand new PR, skip backup if it is.
    if [ "${TRAVIS_PULL_REQUEST}" != "false" ]; then
        joplin_log ${FUNCNAME[0]} 1 "This is a brand-new pull request, since there is no database, there will be no backup.";
        joplin_log ${FUNCNAME[0]} 1 "Skipping Backup Process.";
    else

        # Not a new PR, not a test, and not an error
        if [ "$?" = "0" ]; then

            # Retrieve App Name
            joplin_build_header "Creating Database Backup in S3"

            APPNAME=$(joplin_resolve_heroku_appname $1);

            # Gather connection string from heroku api
            CONNECTION_STRING=$(heroku config:get DATABASE_URL -a $APPNAME);
            DB_NAME=$(echo -n $CONNECTION_STRING | cut -d "/" -f 4);
            DB_TIMESTAMP=$(date '+%Y-%m-%d--%H-%M-%S');
            DJANGO_MID=$(retrieve_latest_django_mid);

            S3_BUCKET_FILE_URL="s3://${AWS_BUCKET_BACKUPS}/backups/database/${TRAVIS_BRANCH}/${APPNAME}.${DB_TIMESTAMP}.${TRAVIS_COMMIT}.${DJANGO_MID}.psql.gz"

            echo "joplin_backup_database() ----- Performing Database Backup for Branch: $1, App: $APPNAME";
            echo "joplin_backup_database() -- App Name: ${APPNAME}";
            echo "joplin_backup_database() -- Date Timestamp: ${DB_TIMESTAMP}";
            echo "joplin_backup_database() -- Latest Django Migration ID: ${DJANGO_MID}";
            echo "joplin_backup_database() -- DB Name: ${DB_NAME}";
            echo "joplin_backup_database() -- S3 File URL: ${S3_BUCKET_FILE_URL}";
            echo "joplin_backup_database() -- Performing copy, please wait...";

            pg_dump $CONNECTION_STRING | gzip | aws s3 cp - $S3_BUCKET_FILE_URL;
            echo "joplin_backup_database()----- Finished creating and uploading database to s3";

            echo "joplin_backup_database()----- Validating the backup has been created and is available on S3";
            heroku_backup_upload_check $S3_BUCKET_FILE_URL
            echo "joplin_backup_database()----- Validation finished, backup process finished.";
        fi;

     fi;
}



#
# Creates a database backup of a running heroku app (as long as it as a PostgreSQL db attached to it)
#
# $1 (string) The name of the branch (ie. "master", "production")
# Example: $ joplin_build master
#

function joplin_build {

    # Validate Branch Name (or halt deployment if no branch specified)
    helper_internal_validation ${FUNCNAME[0]} $1

    # Not a test, and not an error
    if [ "$?" = "0" ]; then
        joplin_build_header "Building Joplin"

        # Retrieve App Name
        APPNAME=$(joplin_resolve_heroku_appname $1);

        echo "joplin_build() ----- Building Docker Container";
        echo "joplin_build() -- Logging in to Services";
        docker login --username=_ --password=$HEROKU_API_KEY registry.heroku.com
        echo "joplin_build() -- Building: '${JOPLIN_IMAGE_NAME}' for Branch: $1, App: $APPNAME";
        docker build -t $JOPLIN_IMAGE_NAME .
        echo "joplin_build() -- Tagging Image";
        docker tag $JOPLIN_IMAGE_NAME registry.heroku.com/$APPNAME/web
        echo "joplin_build() -- Pushing to Heroku Repository";
        docker push registry.heroku.com/$APPNAME/web
        echo "joplin_build()----- Finished Building Container";
    fi;
}



#
# Calls the release function for a specific image to a specific application
# $1 (string) The name of the branch (ie. "master", "production", "pr-160")
# Example: $ joplin_release master
#

function joplin_release {

    # Validate Branch Name (or halt deployment if no branch specified)
    helper_internal_validation ${FUNCNAME[0]} $1

    # Not a test, and not an error
    if [ "$?" = "0" ]; then
        # Retrieve App Name
        APPNAME=$(joplin_resolve_heroku_appname $1);

        # Determine image id to push
        DOCKER_IMAGE_ID=$(docker inspect registry.heroku.com/$APPNAME/web --format={{.Id}})

        echo "joplin_release() ----- Releasing Build for Branch: $1, App: $APPNAME";
        echo "joplin_release() ----- Docker Image Id: $DOCKER_IMAGE_ID";

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
# Example: $ joplin_migrate staging
#

function joplin_migrate {

    # Validate Branch Name (or halt deployment if no branch specified)
    helper_internal_validation ${FUNCNAME[0]} $1

    # Not a test, and not an error
    if [ "$?" = "0" ]; then
        # Retrieve App Name
        APPNAME=$(joplin_resolve_heroku_appname $1);

        echo "joplin_migrate() ----- Migrating data for Branch: $1, App: $APPNAME";
        heroku run -a $APPNAME -- /app/migrate-load-data.sh
        echo "joplin_migrate() ----- Migration process finished.";
    fi;
}


#
# helper_test - Tests the helper has been initialized properly and ready to run
# Runs the functions without parameters forcing error output.
#

function helper_test {
    echo "helper_test() ----- Heroku Helper Test Initialized"
    echo "helper_test() ----- Test tag: ${TRAVIS_CI_TEST_TAG}";

    joplin_build_header "Heroku Helper Testing"

    echo "helper_test() ----- Testing 'joplin_release' is ready: ";
    joplin_release $TRAVIS_CI_TEST_TAG;

    echo "helper_test() ----- Testing 'joplin_backup_database' is ready: ";
    joplin_backup_database $TRAVIS_CI_TEST_TAG;

    echo "helper_test() ----- Testing django migration id: ";
    retrieve_latest_django_mid;

    echo "helper_test() ----- Testing 'joplin_build' is ready: ";
    joplin_build $TRAVIS_CI_TEST_TAG;

    echo "joplin_migrate() ----- Testing 'joplin_migrate' is ready: ";
    joplin_migrate $TRAVIS_CI_TEST_TAG;

    echo "joplin_migrate() ----- Testing 'joplin_create_pr_app' is ready: ";
    joplin_create_pr_app $TRAVIS_CI_TEST_TAG;

    echo "helper_test() ----- Heroku Helper Test finished.";
}


