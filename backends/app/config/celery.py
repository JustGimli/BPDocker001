import os
import sys
from celery import Celery
import dotenv

dotenv.load_dotenv()
sys.path.append('/home/jg/progects/BP/')


app = Celery('config')
app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()
