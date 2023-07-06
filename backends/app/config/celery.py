import os
import sys
from celery import Celery
from kombu import Queue, Exchange
import dotenv

dotenv.load_dotenv()
sys.path.append('/home/jg/progects/BP/')


app = Celery('config')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.conf.task_queues = (
    Queue('celery', routing_key='celery'),
    Queue('delivery', Exchange('delivery', routing_key='delivery', delivery_mode=1, durable=False))
)
app.autodiscover_tasks()
