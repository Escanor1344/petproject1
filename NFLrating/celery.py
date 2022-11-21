import os
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'NFLrating.settings')

app = Celery('NFLrating')

app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()

app.conf.beat_schedule = {
    'send-message-after-7-days': {
        'task': 'mainapp.tasks.send_beat_mail',
        'schedule': crontab(minute=0, hour=0),
    },
}
