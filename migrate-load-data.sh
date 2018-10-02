#!/usr/bin/env bash

echo "Running migrations: (${DEPLOYMENT_MODE}) ..."
python ./joplin/manage.py migrate --noinput


case "${DEPLOYMENT_MODE}" in

    # Determine if we are running in a cloud instance...
    PRODUCTION|STAGING|REVIEW)
        # We have a cloud instance
        python ./joplin/manage.py collectstatic --noinput;
    ;;

    *)
        # We are running locally
        echo "Static files are only collected on STAGING or PRODUCTION, current environment: ${DEPLOYMENT_MODE}";
    ;;

esac;
