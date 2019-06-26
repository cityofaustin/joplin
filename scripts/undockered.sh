#!/usr/bin/env bash

set -o errexit

CURRENT_DIR=`dirname $BASH_SOURCE`
UNDOCK=on sh $CURRENT_DIR/serve-local.sh
