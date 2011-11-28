from openportfolio.settings import *

DEBUG = True


STATIC_ROOT = '/usr/local/web/django/www/staging/openportfolio/static'
MEDIA_ROOT = '/usr/local/web/django/www/staging/openportfolio/media'

TEMPLATE_DIRS = ('/usr/local/web/django/www/staging/openportfolio/openportfolioapp/templates')


DATABASE_ENGINE = 'mysql'           # 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
DATABASE_NAME = 'staging_openportfolio'             # Or path to database file if using sqlite3.
DATABASE_USER = 'openportfolio'             # Not used with sqlite3.
DATABASE_PASSWORD = 'openportfolio'         # Not used with sqlite3.
DATABASE_HOST = 'localhost'             # Set to empty string for localhost. Not used with sqlite3.
DATABASE_PORT = ''             # Set to empty string for default. Not used with sqlite3.
