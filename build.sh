#!/usr/bin/env bash
# exit on error
set -o errexit

pip install --upgrade pip setuptools wheel && pip install -r requirements.txt

python manage.py migrate
python manage.py loaddata fix.json
