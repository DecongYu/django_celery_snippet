"""
The celery.py module needs to be in the same directory of 'wsgi.py'

https://docs.celeryproject.org/en/stable/django/first-steps-with-django.html
"""

import os
from celery import Celery
from celery.signals import task_postrun
from django.conf import settings

from polls.consumers import notify_channel_layer



# this code copied from manage.py
# to set the default Django setttings module for the 'celery' app
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'django_celery.settings')

app = Celery("django_celery")

# read config from Django settings, the CELERY namespace would make celery config keys
# has 'CELERY' prefix - a lazy way to set celery setttings (without a separate settings)
app.config_from_object('django.conf:settings', namespace='CELERY')

# discover and load 'tasks.py;' in django apps, any tasks.py will be automatically add to setttings.apps
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)

# test
@app.task
def divide(x, y):
    # # debug tool rdb to set up breaking point
    # from celery.contrib import rdb
    # rdb.set_trace()

    # task
    import time
    time.sleep(5)
    return x / y

@task_postrun.connect
def task_postrun_handler(task_id, **kwargs):
    """
    When celery task finish, send notification to Django Channel_layer, so Django channel would 
    recieve the event and send it to the web client
    """
    notify_channel_layer(task_id)
