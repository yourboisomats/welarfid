#!/usr/bin/env bash
SCRIPT_PATH="$( cd "$(dirname "$0")" ; pwd -P )"
cd $SCRIPT_PATH
source $SCRIPT_PATH/env/bin/activate
until python ./listen_mqtt.py; do
    echo "'wela mqtt' crashed with exit code $?. Restarting..." >&2
    sleep 1
done
