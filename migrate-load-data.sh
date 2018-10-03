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
        echo "Static files are only collected on STAGING, PRODUCTION or REVIEW, current environment: ${DEPLOYMENT_MODE}";
    ;;

esac;

# Trying a fixture import instead of a migration...

if [ "${DEPLOYMENT_MODE}" = "REVIEW" ]; then
    python ./joplin/manage.py loadcontent \
        fixtures/images.yaml \
        fixtures/311.yaml \
        fixtures/themes.yaml \
        fixtures/topics.yaml \
        fixtures/locations.yaml \
        fixtures/contacts.yaml \
        fixtures/departments.yaml \
        fixtures/services \
        fixtures/processes
fi;
