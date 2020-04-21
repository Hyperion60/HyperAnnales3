#!/bin/sh

#Python3.7 install
sudo apt update
sudo apt-get -y install build-essential zlib1g-dev libncurses5-dev libgdm-dev libnss3-dev libssl-dev libreadline-dev libffi-dev curl
curl -O https://www.python.org/ftp/python/3.7.3/Python-3.7.3.tar.xz
tar -xf Python-3.7.3.tar.xz
cd Python-3.7.3
./configure --enable-optimizations
make
sudo make install

cd ..
rm -rf Python-3.7.3.tar.xz Python-3.7.3

#Install pip for Python3.7
sudo apt update && sudo apt -y install python3-pip libssl-dev

# Install git
sudo apt -y install git-core

# Download static file, templates, database
cd /home/HyperAnnales
mkdir templates
cd templates
git clone git@github.com:Hyperion60/Templates_HA.git

cd /home/HyperAnnales
mkdir static
cd static
git clone git@github.com:Hyperion60/static_HA.git

cd /home/HyperAnnales
mkdir db
cd db
git clone git@github.com:Hyperion60/db_HA.git