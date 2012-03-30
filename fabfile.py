"""
This fabfile automates the deployment of github hosted django projects

Author: Evan Davey, evan.j.davey@gmail.com


Instructions:

Modify the environment variables in development,staging or production to
reflect your working environment

To run the project on a development or local machine.

$ fab development bootstrap
$ fab development runserver 

"""

import os,sys

from fabric.api import *
from fabric.contrib.project import rsync_project
from fabric.contrib import files, console
from fabric import utils
from fabric.decorators import hosts
from contextlib import contextmanager as _contextmanager
from fabric.colors import *
from fabtools import *

env.project = 'openportfolio'
env.repo = 'git://github.com/evandavey/OpenPortfolio.git'
env.apacheconfig = '/usr/local/web/config'
env.home = '/usr/local/web/django'

def _setup_path():
	env.root = os.path.join(env.home, 'www', env.environment)
	env.code_root = os.path.join(env.root, env.project)
	env.virtualenv_root = os.path.join(env.root, 'env')
	env.settings = '%(project)s.settings_%(environment)s' % env


def development():
	""" Development settings.  Modify these to match your environment """
	env.environment = 'development'
	env.user = 'evandavey'
	env.serverport = '8081'

def staging():
	""" use staging environment on remote host"""

	env.environment = 'staging'
	env.hosts = ['192.168.0.20']
	env.servername = 'openportfolio-staging.getoutsideandlive.com'
	env.branch = 'develop'
	env.db = 'staging_openportfolio'
	env.db_user = 'openportfolio'
	env.db_password = 'openportfolio'
	env.db_backup = '/usr/local/backup/db_dumps/staging_openportfolio.txt'
	_setup_path()

def production():
	env.environment = 'production'
	env.hosts = ['192.168.0.20']
	env.servername = 'openportfolio.getoutsideandlive.com'
	env.branch = 'master'
	env.db = 'openportfolio'
	env.db_user = 'openportfolio'
	env.db_password = 'openportfolio'
	env.db_backup = '/usr/local/backup/db_dumps/openportfolio.txt'
	_setup_path()


def sync_staging_database():
    
    production()
    dump_data()
    staging()
    env.db_backup = '/usr/local/backup/db_dumps/openportfolio.txt'
    load_data()
    
def load_fixtures():
    fix='openportfolioapp/fixtures/'
    
    fixtures=['portfolio.yaml',
            'assetclass.yaml',
            'gicssector.yaml',
            'company.yaml',
            'currency.yaml',
            'investment.yaml',
            'listedequity.yaml',
            'savingsaccount.yaml'
            ]
    
    for f in fixtures:
        manage('loaddata %s' % os.path.join(fix,f))
    
 
def fetch_prices():

    manage('fetch-prices 20091231 20120320')
    
