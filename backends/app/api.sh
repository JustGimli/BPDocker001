#!/bin/sh

# until cd /home/app
# do
#     echo "Waiting for server volume..."
# done

until python3 manage.py makemigrations
do
    echo "Waiting for db to be ready..."
    sleep 3
done

until python3 manage.py migrate
do
    echo "Waiting for db to be ready..."
    sleep 3
done




gunicorn config.wsgi --bind 0.0.0.0:8000 --workers 4 --threads 4

