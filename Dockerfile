FROM ubuntu:20.04

MAINTAINER Vadim Nikulin "vanikulin@rambler.ru"

ARG DEBIAN_FRONTEND=noninteractive

RUN apt-get update -y && \
    apt-get install -y python3-pip python3-dev && \
    apt-get install -y nginx uwsgi uwsgi-plugin-python3

COPY ./requirements.txt /requirements.txt
COPY ./nginx.conf /etc/nginx/nginx.conf

WORKDIR /

RUN pip3 install -r requirements.txt

COPY . /

RUN adduser --disabled-password --gecos '' nginx\
  && chown -R nginx:nginx /app \
  && chmod 777 /run/ -R \
  && chmod 777 /root/ -R

RUN mkdir -p /usr/share/nginx/logs && chown nginx:nginx /usr/share/nginx/logs

ENTRYPOINT [ "/bin/bash", "/launch.sh" ]

