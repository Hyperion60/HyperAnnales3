#!/bin/sh

set -e

sleep 10
apt -y install tree
cat HyperAnnales/HyperAnnales/uwsgi.ini
tree HyperAnnales
