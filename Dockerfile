FROM python:3.7-slim-buster

RUN apt-get update
RUN apt-get -y install gcc

WORKDIR /opt/app

COPY . /opt/app
RUN pip install -r requirements.txt

ENV FLASK_APP=server.py
ENV FLASK_ENV=deployment
