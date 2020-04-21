#!/bin/sh

#Python3.7 install
apt update
apt-get -y install build-essential zlib1g-dev libncurses5-dev libgdm-dev libnss3-dev libssl-dev libreadline-dev libffi-dev curl sudo apt-utils
curl -O https://www.python.org/ftp/python/3.7.3/Python-3.7.3.tar.xz
tar -xf Python-3.7.3.tar.xz
cd Python-3.7.3
./configure --enable-optimizations
make
make install

cd ..
rm -rf Python-3.7.3.tar.xz Python-3.7.3

#Install pip for Python3.7
apt update && apt -y install python3-pip libssl-dev

# Install git
apt -y install git-core