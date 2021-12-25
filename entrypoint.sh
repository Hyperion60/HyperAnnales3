#!/bin/sh
set -e

sleep 5

# Handle when the database just created
mkdir /tmp/static
mv static_files/apps.py /tmp/static/
mv accounts/apps.py /tmp/
# ----

cd HyperAnnales && python manage.py makemigrations
python manage.py makemigrations static_files
python manage.py migrate --database=user_ref

# ----
mv /tmp/static/apps.py static_files/
mv /tmp/apps.py accounts/
# ----

uwsgi --wsgi-file "/home/HyperAnnales/HyperAnnales/wsgi.py" --http-socket 0.0.0.0:6094 --chdir "/home/HyperAnnales" --show-config
