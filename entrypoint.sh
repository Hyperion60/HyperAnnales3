#!/bin/sh
set -e

sleep 5

cd HyperAnnales && python manage.py makemigrations
python manage.py makemigrations static_files
python manage.py migrate --database=user_ref

uwsgi --wsgi-file "/home/HyperAnnales/HyperAnnales/wsgi.py" --http-socket 0.0.0.0:6094 --chdir "/home/HyperAnnales" --show-config
