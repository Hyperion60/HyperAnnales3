#!/bin/sh

# Download static file, templates, database
cd /home/HyperAnnales
git clone git@github.com:Hyperion60/Templates_HA.git

cd /home/HyperAnnales
git clone git@github.com:Hyperion60/static_HA.git

cd /home/HyperAnnales
git clone git@github.com:Hyperion60/db_HA.git

cd /
mkdir media
cd media
git clone git@github.com:Hyperion60/media_HA.git