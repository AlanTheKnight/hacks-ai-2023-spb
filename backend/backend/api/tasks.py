import logging
from time import sleep

from backend.celery import celery_app


@celery_app.task(bind=True)
def test():
    print("test")
    sleep(5)
    print("test2")
