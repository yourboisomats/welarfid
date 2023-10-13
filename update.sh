#!/usr/bin/env bash
cd "$(dirname "$0")"
git reset --hard
git pull
source env/bin/activate
pip install -r requirements.txt