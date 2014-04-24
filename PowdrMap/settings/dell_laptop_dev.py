from .base import *
import djcelery

from datetime import timedelta

djcelery.setup_loader()
BACKEND = 'amqp'
BROKER_URL = 'amqp://'
CELERYBEAT_SCHEDULER = 'djcelery.schedulers.DatabaseScheduler'
#CELERY_RESULT_BACKEND='djcelery.backends.database:DatabaseBackend'
CELERY_TIMEZONE = 'America/Denver'

CELERYBEAT_SCHEDULE = {
    'grab_and_parse_xml': {
        'task': 'PowdrMap.apps.cdot_counting.tasks.gen_speed_values',
        'schedule': timedelta(minutes=2)
    },
}


INSTALLED_APPS += (
    'PowdrMap.apps.mountain_chooser',
    'PowdrMap.apps.cdot_counting',
    'djcelery',
    'kombu.transport.django',
)


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'cdot_counting_db',  # Or path to database file if using sqlite3.
        'USER': 'sherrick',          # Not used with sqlite3.
        'PASSWORD': 'pumpkin',       # Not used with sqlite3.
        'HOST': '',                  # Set to empty string for localhost.
        'PORT': '',                  # Set to empty string for default.
    }
}

#DATABASES.update({
#         'some_name': {
#            'ENGINE': 'django.db.backends.postgresql_psycopg2',
#            'NAME': 'resort_db',                      # Or path to database file if using sqlite3.
#            'USER': 'postgres',                      # Not used with sqlite3.
#            'PASSWORD': 'pumpkin',                  # Not used with sqlite3.
#            'HOST': '',                      # Set to empty string for localhost. Not used with sqlite3.
#            'PORT': '',                      # Set to empty string for default. Not used with sqlite3.
#         }
#    }
#)
