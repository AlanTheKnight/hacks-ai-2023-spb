from __future__ import absolute_import, unicode_literals

import os

from celery import Celery
from gradio_client import Client


from backend.settings import config, BASE_DIR

MEDIA_DIR = BASE_DIR / "media" / "logos"
print(MEDIA_DIR)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')

mlclient_lm = Client(config["Gradio"]["LANGUAGE_MODEL"], verbose=False)
mlclient_sd = Client(config["Gradio"]["KANDINSKY_MODEL"], verbose=False, output_dir=MEDIA_DIR)

celery_app = Celery('API')

celery_app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django app configs.
celery_app.autodiscover_tasks()
