#!/usr/bin/env bash

# Determine ENV by your git branch
function get_env {
  if [ $CIRCLE_BRANCH == "master" ]; then
    echo "staging"
  elif [ $CIRCLE_BRANCH == "production" ]; then
    echo "prod"
  else
    echo "dev"
  fi
}
