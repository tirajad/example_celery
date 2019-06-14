import djcelery
from celery.schedules import crontab
from datetime import timedelta

from .common_settings import *  # pylint: disable=W0401

djcelery.setup_loader()

INSTALLED_APPS += [
    'jay',
    'djcelery',
]


try:
    from configs import *  # pylint: disable=W0401
except ImportError:
    pass

USE_CELERY = getattr(configs, 'USE_CELERY', False)
BROKER_URL = getattr(configs, 'BROKER_URL', 'redis://localhost:6379/0')

CELERY_ACCEPT_CONTENT = ['json', 'msgpack', 'yaml']
CELERY_TASK_SERIALIZER = 'json'
CELERY_TIMEZONE = 'Asia/Bangkok'
CELERY_CREATE_MISSING_QUEUES = True

CELERY_ROUTES = {
    'jay.tasks.test.celery': {'queue': '1'},
    'jay.tasks.test.celery_1': {'queue': '2'},
}

CELERYBEAT_SCHEDULE = {
    # 'celery-beat': {
    #     'task': 'jay.tasks.test.celery_1',
    #     'schedule': timedelta(seconds=10),
    #     'args': [],
    # },
    'celery-beat': {
        'task': 'jay.tasks.test.celery_1',
        'schedule': crontab(hour=0, minute=30),  # ทุกๆเที่ยงคืนครึ่ง
        'args': [],
    },
}