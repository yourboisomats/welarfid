#!/usr/bin/env bash
SCRIPT_PATH="$( cd "$(dirname "$0")" ; pwd -P )"
cd $SCRIPT_PATH
source $SCRIPT_PATH/env/bin/activate
python ./reading.py