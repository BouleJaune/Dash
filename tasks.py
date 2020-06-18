import datetime
import time
import os

from celery import Celery


celery_app = Celery('hello', broker='redis://127.0.0.1:6382/0')


@celery_app.task
def hello():
    time.sleep(10)
    with open ('hellos.txt', 'a') as hellofile:
        hellofile.write('Hello {}\n'.format(datetime.datetime.now()))
