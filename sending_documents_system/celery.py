# django_celery/celery.py

import os
from celery import Celery

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "sending_documents_system.settings")
app = Celery("sending_documents_system")
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()

app.conf.enable_utc = False

app.conf.update(timezone = 'Africa/Nairobi')

app.autodiscover_tasks()