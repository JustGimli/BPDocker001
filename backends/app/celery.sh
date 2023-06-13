#!/bin/sh


# until python3 manage.py migrate
# do
#     echo "Waiting for db to be ready..."
#     sleep 3
# done

celery -A config worker --loglevel=info