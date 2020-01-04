import json
import os
from datetime import datetime, timedelta

from celery import Celery

# app = Celery('tasks', broker='amqp://192.168.99.100:32769')
app = Celery('tasks', broker='pyamqp://guest@localhost//')

@app.task
def add(x, y):
    return x + y