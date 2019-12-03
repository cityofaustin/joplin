#!/usr/bin/env bash
CD=`dirname $BASH_SOURCE`

# Converts Pipfile into a requirements.txt
# This is for installing dependencies with pip (rather than pipenv)
# when we're building a docker container.
pipenv lock --requirements > $CD/../build_artifacts/requirements.txt
