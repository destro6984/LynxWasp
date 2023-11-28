#!/usr/bin/env bash
# exit on error
set -o errexit

pip install --upgrade pip setuptools wheel && pip install -r requirements.txt

echo "Wait 10 sec"
sleep 10
python manage.py collectstatic --no-input
python manage.py migrate
python manage.py loaddata fix.json
