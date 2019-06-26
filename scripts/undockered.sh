#!/usr/bin/env bash

set -o errexit

D=`dirname $BASH_SOURCE`
UNDOCK=on sh $D/serve-local.sh
