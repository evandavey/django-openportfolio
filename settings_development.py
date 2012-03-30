from openportfolio.settings import *

DEBUG = True


MEDIA_ROOT = "media"
TEMPLATE_DIRS=('/Users/evandavey/Documents/openportfolio/openportfolioapp/templates/')

DATABASE_ENGINE = 'sqlite3'
DATABASE_NAME = 'openportfolio.db'

DATABASE_ENGINE = 'mysql'           # 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
DATABASE_NAME = 'openportfolio'             # Or path to database file if using sqlite3.
DATABASE_USER = 'openportfolio'             # Not used with sqlite3.
DATABASE_PASSWORD = 'openportfolio'         # Not used with sqlite3.
DATABASE_HOST = '192.168.0.20'             # Set to empty string for localhost. Not used with sqlite3.
DATABASE_PORT = ''             # Set to empty string for default. Not used with sqlite3.

