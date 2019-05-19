#!/usr/bin/env bash

# Determine ENV by your git branch
function get_env {
  if [ $CIRCLE_BRANCH == "master" ]; then
    return "staging"
  elif [ $CIRCLE_BRANCH == "production" ]; then
    return "prod"
  else
    return "dev"
  fi
}
