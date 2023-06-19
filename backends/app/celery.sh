#!/bin/sh


until pip install channels[daphne]
do
    echo "Waiting for db to be ready..."
    sleep 3
done
celery -A config worker --loglevel=info
