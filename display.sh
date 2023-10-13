#!/usr/bin/env bash
SCRIPT_PATH="$( cd "$(dirname "$0")" ; pwd -P )"
cd $SCRIPT_PATH
source $SCRIPT_PATH/env/bin/activate
sleep 10
until python ./display.py > display.log; do
    echo "'wela mqtt' crashed with exit code $?. Restarting..." >&2
    sleep 1
done
