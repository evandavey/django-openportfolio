from openportfolio.settings import *

DEBUG = False


STATIC_ROOT = '/usr/local/web/django/www/production/openportfolio/static'
MEDIA_ROOT = '/usr/local/web/django/www/production/openportfolio/media'

TEMPLATE_DIRS = ('/usr/local/web/django/www/production/openportfolio/openportfolioapp/templates')

DATABASE_ENGINE = 'mysql'           # 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
DATABASE_NAME = 'openportfolio'             # Or path to database file if using sqlite3.
DATABASE_USER = 'openportfolio'             # Not used with sqlite3.
DATABASE_PASSWORD = 'openportfolio'         # Not used with sqlite3.
DATABASE_HOST = 'localhost'             # Set to empty string for localhost. Not used with sqlite3.
DATABASE_PORT = ''             # Set to empty string for default. Not used with sqlite3.

