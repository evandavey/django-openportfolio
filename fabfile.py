"""
This fabfile automates the deployment of github hosted django projects

Author: Evan Davey, evan.j.davey@gmail.com

"""

import os,sys

from fabric.api import *
from fabric.contrib.project import rsync_project
from fabric.contrib import files, console
from fabric import utils
from fabric.decorators import hosts
from contextlib import contextmanager as _contextmanager
from fabric.colors import *


env.project = 'openportfolio'
env.git_url = 'git://github.com/evandavey/OpenPortfolio.git'



def _setup_path():
	env.root = os.path.join(env.home, 'www', env.environment)
	env.code_root = os.path.join(env.root, env.project)
	env.virtualenv_root = os.path.join(env.root, 'env')
	env.settings = '%(project)s.settings_%(environment)s' % env


def development():
	env.home = '/Users/evandavey/django-dev/'
	env.environment = 'development'
	env.hosts = ['localhost']
	env.user = 'evandavey'
	env.serverport = '8081'
	_setup_path()

def staging():
	""" use staging environment on remote host"""

	env.home = '/usr/local/web/django'
	env.user = 'evandavey'
	env.environment = 'staging'
	env.hosts = ['192.168.0.21']
	env.servername = 'openportfolio.getoutsideandlive.com'
	_setup_path()


def production():
	""" use production environment on remote host"""
	utils.abort('Production deployment not yet implemented.')


def bootstrap():
	""" sets up host system virtual environment and directory structure """
	
	print(green("Creating project directories"))
	run('mkdir -p %(root)s' % env)
	run('mkdir -p %s' % os.path.join(env.home, 'www', 'log'))
	create_virtualenv()
	clone_remote()
	update_requirements()
	
	
def create_virtualenv():
	""" creates a virtual environment """
	
	print(green("Creating a virtual environment in %s" % env.virtualenv_root))
	sudo('WORKON_HOME=%s' % (env.virtualenv_root) + ' && ' + 'source /usr/local/bin/virtualenvwrapper.sh && ' + 'mkvirtualenv %s' % (env.project),user=env.user)
	

def clone_remote():
	""" Downloads project code from its git repository """
	
	print(green("Cloning repository %s" % env.git_url))
	
	run('rm -rf %s' % os.path.join(env.root,env.project))
	run('git clone %s %s/%s' % (env.git_url,env.root,env.project))


def update_requirements():
	""" update external dependencies  """
	
	print(green("Installing dependencies"))
	requirements = os.path.join(env.code_root, 'requirements')
	with cd(requirements):
		cmd = ['pip install']
		cmd +=['-q']
		cmd += ['-r %s' % os.path.join(requirements, '%s.txt' % env.environment)]

		with virtualenv():
			run(' '.join(cmd))
	
	
def syncdb():
	""" syncs the django database """
	
	print(green("Syncing %s database" % env.project))
	
	with virtualenv():
		with cd(env.code_root):
			run('./manage.py syncdb --settings=%s.settings_%s' % (env.project,env.environment))

def migratedb():
	""" syncs the django database """
	
	print(green('Migrating apps in db'))

	with virtualenv():
		with cd(env.code_root):
			run('./manage.py migrate --all --settings=%s.settings_%s' % (env.project,env.environment))


def runserver():
	""" runs the project as a development server """

	require('serverport',provided_by=development)

	print(green('Running development server.  Access at http://127.0.0.1:%s' % env.serverport))

	with virtualenv():
		with cd(env.code_root):
			run('./manage.py runserver 0.0.0.0:%s --settings=%s.settings_%s' % (env.serverport,env.project,env.environment))


	
@_contextmanager
def virtualenv():
	""" Wrapper function to ensure code is run under a virtual environment """
	
	venv_dir=os.path.join(env.virtualenv_root, env.project)
	activate='source ' + os.path.join(venv_dir,'bin','activate')

	with prefix(activate):
	    yield
	


	


