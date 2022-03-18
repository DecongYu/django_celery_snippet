import json
import random

from django.contrib.auth.models import User

import requests, celery
from celery import shared_task, Task
from celery.signals import task_postrun
from polls.consumers import notify_channel_layer
from celery.utils.log import get_task_logger

logger = get_task_logger(__name__)


##### tools #####
# task retry decorator - a class
class BaseTaskWithRetry(celery.Task):
    autoretry_for  = (Exception, KeyError)
    retry_kwargs = {'max_tries': 5}
    retry_backoff = True



##### tasks #####
@shared_task()
def sample_task(email):
    from polls.views import api_call

    api_call(email)

# # decorator retry failed task
# @shared_task(bind=True, autoretry_for =(Exception,), retry_backoff=5, retry_jitter=True, retry_kwargs={'max_retries': 5})
# def task_process_notification(self):
#     if not random.choice([0, 1]):
#         # mimic random error
#         raise Exception()

#     requests.post('https://httpbin.org/delay/5')

# Task base class - retry class
@shared_task(bind=True, base=BaseTaskWithRetry)
def task_process_notification(self):
    if not random.choice([0, 1]):
        # miniac a random error for testing
        raise Exception()
    
    requests.post('https://httpbin.org/delay/5')


@task_postrun.connect
def task_postrun_handler(task_id, **kwargs):
    """
    When celery task finish, send notification to Django channel_layer, so Django channel
    would receive the event and send it to webclient.
    """
    notify_channel_layer(task_id)


@shared_task(name='task_clear_session')
def task_clear_session():
    from django.core.management import call_command
    call_command('clearsessions')


@shared_task(name='default:dynamic_example_one')
def dynamic_example_one():
    logger.info('Example One')

@shared_task(name='low_priority:dynamic_example_two')
def dynamic_example_two():
    logger.info('Example Two')

@shared_task(name='high_priority:dynamic_example_three')
def dynamic_example_three():
    logger.info('Example Three')

@shared_task()
def task_send_welcome_email(user_pk):
    user = User.objects.get(pk=user_pk)
    logger.info(f'send email to {user.email} {user.pk}')


# @shared_task()
# def task_transaction_test():
#     from .views import random_username
#     username = random_username()
#     user = User.objects.create_user(username, 'lennon@thebeatles.com', 'johnpassword')
#     user.save()
#     logger.info(f'send email to {user.pk}')
#     raise Exception('test')