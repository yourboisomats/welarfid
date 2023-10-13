#!/bin/bash
# script for updating vendowifi app
working_folder="/opt/reader"
rm "$working_folder/reader/*.log"
[ -d "$working_folder" ] || mkdir "$working_folder"
cd "$working_folder"
latest_version=$(curl -s http://wela.online/files/version.txt)
if [ -f "version.txt" ]
then
	current_version=$(tail version.txt)
else
	current_version=0
	echo "0" > version.txt
fi

echo "latest version $latest_version and your version $current_version"

if [ "$latest_version" == "$current_version" ]
then
    echo "your version is updated"
else
    echo "upgrading to rfid reader v$latest_version"
    wget http://wela.online/files/desktop.tgz -O /tmp/desktop.tgz
    tar xf /tmp/desktop.tgz -C $working_folder
    echo "$latest_version" > version.txt
    rm -f *.log
fi
