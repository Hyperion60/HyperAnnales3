FROM python:3.7
ENV PYTHONUNBUFFERED 1

COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

# Install packages and dependencies
ADD ./requirements.txt /requirements.txt

# Install pip for Python 3.7
RUN apt update && apt -y upgrade
RUN apt-get -y install python3-pip libssl-dev curl apt-utils

# Install psycopg2
RUN apt-get -y install gcc python3-dev musl-dev

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
RUN chmod 700 ~/.ssh
RUN mv /tmp/vps-key ~/.ssh/ && mv ~/.ssh/vps-key ~/.ssh/id_rsa
RUN chmod 600 ~/.ssh/id_rsa
RUN eval `ssh-agent -s` && ssh-add ~/.ssh/id_rsa

# Copy codes and sources of website
WORKDIR /home
COPY . /home


# Download static file
RUN mkdir /media/ && cd /media/ && git clone git@github.com:Hyperion60/static_HA.git

RUN cd /media && git clone git@github.com:Hyperion60/media_HA.git

# Expose port
EXPOSE 6094

ENTRYPOINT ["/entrypoint.sh"]
