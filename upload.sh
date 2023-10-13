#!/usr/bin/env bash
SCRIPT_PATH="$( cd "$(dirname "$0")" ; pwd -P )"
cd $SCRIPT_PATH
find data/ -type f -empty -delete
source $SCRIPT_PATH/env/bin/activate
python ./upload_attendance.py
