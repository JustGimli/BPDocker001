#!/bin/sh   
celery -A config worker -l INFO --concurrency 1 -E

