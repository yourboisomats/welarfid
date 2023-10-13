#!/usr/bin/env bash

while true; do
        if ps aux | grep "[p]ython /opt/welarfid/frontend.py"
        then
                echo "Running"
        else
                echo "Stopped"
                python /opt/welarfid/frontend.py
        fi
sleep 1
done