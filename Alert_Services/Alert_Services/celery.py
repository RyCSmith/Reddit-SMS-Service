from __future__ import absolute_import
import os
from celery import Celery
from django.apps import AppConfig
from django.conf import settings

#Celery configuration settings for Alert_Services project

if not settings.configured:
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "Alert_Services.settings")

app = Celery('Alert_Services')

class CeleryConfig(AppConfig):
    name = 'Alert_Services'
    verbose_name = 'Celery Config'
    def ready(self):
        app.config_from_object('django.conf:settings')
        app.autodiscover_tasks(lambda: settings.INSTALLED_APPS, force=True)


app.config_from_object('django.conf:settings')
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS, force=True)

@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))