FROM python:3.7
ENV PYTHONUNBUFFERED 1


# Install packages and dependencies
ADD ./requirements.txt /requirements.txt


# Python 3.7 install
# RUN apt update
# RUN apt-get -y install build-essential zlib1g-dev libncurses5-dev libgdm-dev libnss3-dev libssl-dev libreadline-dev libffi-dev curl sudo apt-utils
# RUN curl -O https://www.python.org/ftp/python/3.7.3/Python-3.7.3.tar.xz
# RUN tar -xf Python-3.7.3.tar.xz
# RUN cd Python-3.7.3 && ./configure --enable-optimizations
# RUN cd Python-3.7.3 && make install
# RUN rm -rf Python-3.7.3.tar.xz Python-3.7.3


# Install pip for Python 3.7
RUN apt update && apt -y upgrade
RUN apt-get -y install python3-pip


# Install git
RUN apt-get -y install git git-core


# Install pip3 packages
RUN pip3 install -U pip
RUN LIBRARY_PATH="/lib:/usr/lib"
RUN /bin/sh -c " pip3 install -r /requirements.txt --no-cache-dir"

# Authorize SSH Host
RUN eval `ssh-agent -s`
RUN mkdir ~/.ssh

COPY ./git/vps-key /tmp/

RUN echo "StrictHostKeyChecking no" >> /etc/ssh/ssh_config
RUN cat /etc/ssh/ssh_config
RUN chmod go-w ~
RUN chmod 700 ~/.ssh && ls -lsha ~/.ssh
RUN ls -lsha ~/.ssh
RUN mv /tmp/vps-key ~/.ssh/ && rm /tmp/vps-key
RUN chmod 600 ~/.ssh/vps-key
RUN eval `ssh-agent -s` && ssh-add ~/.ssh/vps-key

# Copy codes and sources of website
WORKDIR /home
COPY ./HyperAnnales /home

COPY ./git/vps-key-simple /root/.ssh/

# Download static file, templates, database
RUN cd /home/HyperAnnales
RUN git clone git@github.com:Hyperion60/Templates_HA.git

RUN cd /home/HyperAnnales
RUN git clone git@github.com:Hyperion60/static_HA.git

RUN cd /home/HyperAnnales
RUN git clone git@github.com:Hyperion60/db_HA.git

RUN cd /
RUN mkdir media
RUN cd media
RUN git clone git@github.com:Hyperion60/media_HA.git


# Copy files for github
COPY ./git /root/.ssh


# Expose port
EXPOSE 6094


# Define command to launch website when starting the container
CMD ["uwsgi", "--ini", "/home/HyperAnnales/uwsgi.ini"]