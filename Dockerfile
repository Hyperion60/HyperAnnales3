FROM python:3.7
ENV PYTHONUNBUFFERED 1
ADD ./requirements.txt /requirements.txt
RUN pip install -U pip &&
LIBRARY_PATH=/lib:/usr/lib /bin/sh -c "pip install -r /requirements.txt --nocache-dir"
RUN mkdir /code
WORKDIR /code
ADD ./HyperAnnales_src /src/