#!/bin/sh

set -e

sleep 5
uwsgi --wsgi-file "/home/HyperAnnales/HyperAnnales/wsgi.py" --http-socket 0.0.0.0:6094 --chdir "/home/HyperAnnales"