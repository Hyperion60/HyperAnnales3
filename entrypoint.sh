#!/bin/sh

set -e

sleep 5
uwsgi --wsgi-file "/home/HyperAnnales/HyperAnnales/wsgi.py" --http-socket 127.0.0.1:6094 --chdir "/home/HyperAnnales"