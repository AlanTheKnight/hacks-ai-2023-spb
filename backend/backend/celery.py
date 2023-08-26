from __future__ import absolute_import, unicode_literals

import os

from celery import Celery
from gradio_client import Client

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')

# ml_client = Client(ML_URL, verbose=False)

celery_app = Celery('API')

celery_app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django app configs.
celery_app.autodiscover_tasks()
