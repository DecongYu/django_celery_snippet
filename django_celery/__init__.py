"""
This will make sure the app (celery) is always imported when 
Django starts so that shared_task will use the app
"""

from .celery import app as celery_app

__all__ = ('celery_app',)