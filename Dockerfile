FROM python:3.7
ENV PYTHONUNBUFFERED 1

# Install packages and dependencies
ADD ./requirements.txt /requirements.txt
ADD ./debian-req.sh /debian-req.sh
RUN chmod +x /debian-req.sh
RUN /debian-req.sh
RUN pip3 install -U pip &&
RUN LIBRARY_PATH="/lib:/usr/lib"
RUN /bin/sh -c " pip3 install -r /requirements.txt --nocache-dir"

# Copy codes and sources of website
RUN mkdir /home/
WORKDIR /home
COPY ./HyperAnnales /home

# Copy files for github
RUN mkdir /ssh/
COPY ./git /ssh

# Expose port
EXPOSE 6060

# Define command to launch website when starting the container
CMD ["uwsgi", "--ini", "/home/HyperAnnales/uwsgi.ini"]