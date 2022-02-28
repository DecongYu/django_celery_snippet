"""
The celery.py module needs to be in the same directory of 'wsgi.py'

https://docs.celeryproject.org/en/stable/django/first-steps-with-django.html
"""

import os
from celery import Celery
from django.conf import settings


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
    import time
    time.sleep(5)
    return x / y

@app.task
def add(x,y):
    import time
    time.sleep(8)
    return x + y

