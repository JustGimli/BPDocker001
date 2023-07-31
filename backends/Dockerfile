FROM python:3-alpine

# set environment variables  
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1  
ENV DJANGO_SETTINGS_MODULE=config.settings
ENV DockerHome='/home/app'
ENV DEBUG="True"
ENV CELERY_BROKER_URL="redis://redis/0"
ENV CELERY_RESULT_BACKEND="redis://redis/1"
ENV SQL_ENGINE=django.db.backends.postgresql
ENV SQL_DATABASE=postgres
ENV SQL_HOST=db
ENV SQL_USER=postgres
ENV SQL_PASSWORD=postgres
ENV SQL_PORT=5432
ENV REDIS_HOST=redis
ENV ALLOWED_HOST='127.0.0.1 89.23.100.32'

RUN pip install --upgrade pip


COPY req.txt .

RUN pip install -r req.txt
# RUN pip uninstall -y channels

ARG CACHEBUST=1

COPY ./app/ ${DockerHome}


RUN chmod +x ${DockerHome}/api.sh
RUN chmod +x ${DockerHome}/celery.sh
RUN chmod +x ${DockerHome}/sockets.sh

WORKDIR ${DockerHome}


