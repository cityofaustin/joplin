#!/usr/bin/env bash

if [ "${DEPLOYMENT_MODE}" != "LOCAL" ]; then
    echo -e "Initializing heroku-exec...\n"
    [ -z "$SSH_CLIENT" ] && source <(curl --fail --retry 3 -sSL "$HEROKU_EXEC_URL")
else
    echo "Deployment mode is ${DEPLOYMENT_MODE}, ignoring heroku-exec ..."
fi;
