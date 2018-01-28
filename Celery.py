import os
from celery import Celery

from vkbot_schedule import settings
from vkbot_schedule.settings import BROKER_URL

celery = Celery('tasks', broker=BROKER_URL)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'vkbot_schedule.settings')
app = Celery('vkbot_schedule')
app.config_from_object('django.conf:settings')
app.conf.timezone = 'Europe/Moscow'
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)
