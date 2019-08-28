#!/usr/bin/env bash
# Note: functions are run as subshells function name {(...)} to prevent global variable pollution

# Deletes all containers for a composition
# Searches by container name prefix
# source scripts/docker-helpers.sh; delete_project_containers joplin
function delete_project_containers {(
  COMPOSE_PROJECT_NAME=$1
  docker ps -aq -f name="${COMPOSE_PROJECT_NAME}*" | while read CONTAINER ; do docker rm -f $CONTAINER ; done
)}

# Stops all containers for a composition
# Searches by container name prefix
# command line usage:
# source scripts/docker-helpers.sh; stop_project_containers joplin_migration
function stop_project_containers {(
  COMPOSE_PROJECT_NAME=$1
  docker ps -q -f name="${COMPOSE_PROJECT_NAME}*" | while read CONTAINER ; do docker stop $CONTAINER ; done
)}
