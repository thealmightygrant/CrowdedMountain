from .base import *

INSTALLED_APPS += (
    'PowdrMap.apps.mountain_chooser',
)

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'resort_db',                      # Or path to database file if using sqlite3.
        'USER': 'postgres',                      # Not used with sqlite3.
        'PASSWORD': 'pumpkin',                  # Not used with sqlite3.
        'HOST': '',                      # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '',                      # Set to empty string for default. Not used with sqlite3.
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
