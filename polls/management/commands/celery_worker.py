import shlex
import sys
import subprocess

from django.core.management.base import BaseCommand
from django.utils import autoreload

def restart_celery():
    cmd = 'pkill -f "celery worker"'
    if sys.platform == 'win32':
        cmd = 'taskkill /f /t /im celery.exe'
    
    subprocess.call(shlex.split(cmd))
    subprocess.call(shlex.split('celery -A django_celery worker --loglevel=info'))


class Command(BaseCommand):

    def handle(self, *arg, **options):
        print('Start celery worker with auroreload...')
        autoreload.run_with_reloader(restart_celery)