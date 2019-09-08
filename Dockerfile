FROM tiangolo/uwsgi-nginx-flask:python3.6-alpine3.8

LABEL maintainer "Daniel Wang <hello@danielwang.dev>"

RUN apk add --update --no-cache g++ gcc libxslt-dev jpeg-dev zlib-dev

RUN pip install --upgrade pip
COPY requirements.txt /
RUN pip install --requirement /requirements.txt

COPY ./app /app

ENV LISTEN_PORT=8000
EXPOSE 8000
