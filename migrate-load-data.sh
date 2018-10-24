#!/usr/bin/env bash

echo "Running migrations: (${DEPLOYMENT_MODE}) ..."
python ./joplin/manage.py migrate --noinput

if [ "$?" != "0" ]; then
    echo "There has been an error running the Django migration. Marking as MIGRATION_EXIT_STATUS_ERROR";
fi;


if [ "${DEPLOYMENT_MODE}" = "REVIEW" ]; then
    echo "Running DB restore for PR Review..."
    python ./joplin/manage.py dbrestore --noinput

    if [ "$?" != "0" ]; then
        echo "There has been an error restoring the database. Marking as MIGRATION_EXIT_STATUS_ERROR";
    fi;

fi;

case "${DEPLOYMENT_MODE}" in

    # Determine if we are running in a cloud instance...
    PRODUCTION|STAGING)
        # We have a cloud instance
        python ./joplin/manage.py collectstatic --noinput;

        if [ "$?" != "0" ]; then
            echo -e "There has been an error collecting static files. Marking as MIGRATION_EXIT_STATUS_ERROR";
        fi;

    ;;

    *)
        # We are running locally
        echo "Static files are only collected on STAGING or PRODUCTION, current environment: ${DEPLOYMENT_MODE}";
    ;;

esac;

