#!/usr/bin/env bash
set -e
if [ -d "out/" ]
then
    rm -rf out
fi
mkdir out
cp *.py out/
cp -r ./alembic ./out/alembic
cp -r ./patch ./out/patch
cp patch.sh ./out/
cp frontend.sh ./out/
cp update.sh ./out/
cp default.png ./out/
cp update.sh ./out/
cd out/ && tar -zcf ../rfid.tgz * && cd ..
scp rfid.tgz frappe@wela.online:/home/frappe/wela01/sites/khs.wela.online/public/files
rm -rf out
git rev-list --count HEAD > version.txt
scp version.txt frappe@wela.online:/home/frappe/wela01/sites/khs.wela.online/public/files
scp update.sh frappe@wela.online:/home/frappe/wela01/sites/khs.wela.online/public/files

if [ -d "out/" ]
then
    rm -rf out
fi
mkdir out
cp desktop.py out/
cp MFRC522.py out/
cp update_desktop.sh ./out/
cd out/ && tar -zcf ../desktop.tgz * && cd ..
scp desktop.tgz frappe@wela.online:/home/frappe/wela01/sites/khs.wela.online/public/files
rm -rf out
scp update_desktop.sh frappe@wela.online:/home/frappe/wela01/sites/khs.wela.online/public/files
