#!/bin/sh

set -e

sleep 10
apt -y install tree
cat HyperAnnales/HyperAnnales/uwsgi.ini
tree HyperAnnales
uwsgi --wsgi-file "/home/HyperAnnales/HyperAnnales/wsgi.py" --http-socket 127.0.0.1:6094 --chdir "/home/HyperAnnales"