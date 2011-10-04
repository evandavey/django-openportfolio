import os

from fabric.api import *
from fabric.contrib.project import rsync_project
from fabric.contrib import files, console
from fabric import utils
from fabric.decorators import hosts
from contextlib import contextmanager as _contextmanager

RSYNC_EXCLUDE = (
    '.DS_Store',
    '.hg',
    '*.pyc',
    '*.example',
    '*.db',
    'media/admin',
    'media/attachments',
    'local_settings.py',
    'fabfile.py',
    'bootstrap.py',
)
env.home = '/usr/local/web/django'
env.project = 'openportfolio'
env.deploy_user='evandavey'


def _setup_path():
    env.root = os.path.join(env.home, 'www', env.environment)
    env.code_root = os.path.join(env.root, env.project)
    env.virtualenv_root = os.path.join(env.root, 'env')
    env.settings = '%(project)s.settings_%(environment)s' % env


def development():
    env.environment = 'development'



def staging():
    """ use staging environment on remote host"""
    env.user = 'evandavey'
    env.environment = 'staging'
    env.hosts = ['192.168.0.21']
	env.servername = ['openportfolio.getoutsideandlive.com']
    _setup_path()


def production():
    """ use production environment on remote host"""
    utils.abort('Production deployment not yet implemented.')


def bootstrap():
    """ initialize remote host environment (virtualenv, deploy, update) """
    require('root', provided_by=('staging', 'production'))
    run('mkdir -p %(root)s' % env)
    run('mkdir -p %s' % os.path.join(env.home, 'www', 'log'))
    create_virtualenvwrapper()
    deploy()
    update_requirements2()


def create_virtualenv():
    """ setup virtualenv on remote host """
    require('virtualenv_root', provided_by=('staging', 'production'))
    #args = '--clear --distribute'
    args = '--distribute --no-site-packages'
    run('virtualenv %s %s' % (args, env.virtualenv_root))

def create_virtualenvwrapper():
	""" setup virtualenv on remote host using virtualenvwrapper """
	
	require('virtualenv_root', provided_by=('staging', 'production'))
	sudo('WORKON_HOME=%s' % (env.virtualenv_root) + ' && ' + 'source /usr/local/bin/virtualenvwrapper.sh && ' + 'mkvirtualenv %s' % (env.project),user=env.deploy_user)
	
@_contextmanager
def virtualenv():
	
	venv_dir=os.path.join(env.virtualenv_root, env.project)
	activate='source ' + os.path.join(venv_dir,'bin','activate')
	
	with prefix(activate):
	    yield
	

def deploy():
    """ rsync code to remote host """
    require('root', provided_by=('staging', 'production'))
    if env.environment == 'production':
        if not console.confirm('Are you sure you want to deploy production?',
                               default=False):
            utils.abort('Production deployment aborted.')
    # defaults rsync options:
    # -pthrvz
    # -p preserve permissions
    # -t preserve times
    # -h output numbers in a human-readable format
    # -r recurse into directories
    # -v increase verbosity
    # -z compress file data during the transfer
    extra_opts = '--omit-dir-times'
    rsync_project(
        env.root,
        exclude=RSYNC_EXCLUDE,
        delete=True,
        extra_opts=extra_opts,
    )
    touch()
    collect_static_files()
    apache_reload()
    
def update_portfolio_prices():
    """ runs the local server """
    require('environment',provided_by=('development'))
    local('./manage.py update-portfolio-prices --settings=%s.settings_local' % (env.project))

def syncdb():
    """ runs the local server """
    require('environment',provided_by=('development'))
    local('./manage.py syncdb --settings=%s.settings_local' % (env.project))

def testcode():
    """ runs the local server """
    require('environment',provided_by=('development'))
    local('./manage.py test-code --settings=%s.settings_local' % (env.project))

def migratedb():
    """ runs the local server """
    require('environment',provided_by=('development'))
    local('./manage.py migrate --all --settings=%s.settings_local' % (env.project))

def schemedb():
    """ runs the local server """
    require('environment',provided_by=('development'))
    local('./manage.py schemamigration financemanager --auto --settings=%s.settings_local' % (env.project))

def runserver():
    """ runs the local server """
    require('environment',provided_by=('development'))
    local('./manage.py runserver 0.0.0.0:8080 --settings=%s.settings_local' % (env.project))

def shell():
    """ runs the local shell """
    require('environment',provided_by=('development'))
    local('./manage.py shell --settings=%s.settings_local' % (env.project))


def update_conf_files():
	""" updates conf files to relect fabfile environment settings """

	require('environment', provided_by=('staging', 'production'))
	require('project', provided_by=('staging', 'production'))
	require('servername', provided_by=('staging', 'production'))

	f=open('apache/template.conf','r')
	o=open('apache/%s.conf' % (env.environment),'w')

	for line in f.readlines():
		line=line.replace('<project>',env.project)
		line=line.replace('<environment>',env.environment)
		line=line.replace('<servername>',env.servername)
		o.write(line+"\n")
		
	f=open('apache/template.wsgi','r')
	o=open('apache/%s.wsgi' % (env.environment),'w')

	for line in f.readlines():
		line=line.replace('<project>',env.project)
		line=line.replace('<environment>',env.environment)
		line=line.replace('<servername>',env.servername)
		o.write(line+"\n")



def update_requirements():
    """ update external dependencies on remote host """
    require('code_root', provided_by=('staging', 'production'))
    requirements = os.path.join(env.code_root, 'requirements')
    with cd(requirements):
        cmd = ['pip install']
	
        cmd += ['-E %(virtualenv_root)s' % env]
        cmd += ['--requirement %s' % os.path.join(requirements, 'apps.txt')]
        run(' '.join(cmd))

def update_requirements2():
	""" update external dependencies on remote host """
	require('code_root', provided_by=('staging', 'production'))
	requirements = os.path.join(env.code_root, 'requirements')
	with cd(requirements):
		cmd = ['pip install']
		cmd +=['-U']
		#cmd += ['-E %(virtualenv_root)s' % env]
		cmd += ['-r %s' % os.path.join(requirements, 'apps.txt')]
		
		with virtualenv():
			run(' '.join(cmd))

def touch():
    """ touch wsgi file to trigger reload """
    require('code_root', provided_by=('staging', 'production'))
    apache_dir = os.path.join(env.code_root, 'apache')
    with cd(apache_dir):
        run('touch %s.wsgi' % env.environment)


def collect_static_files():
    """ collect static files on remote host """
    with virtualenv():
        run ('%s/manage.py collectstatic --settings=%s.settings_%s' % (env.code_root,env.project,env.environment))


def update_apache_conf():
    """ upload apache configuration to remote host """
    require('root', provided_by=('staging', 'production'))
    source = os.path.join('apache', '%(environment)s.conf' % env)
    dest = os.path.join(env.home, '../config/sites','0002_any_443_financedb.getoutsideandlive.com.conf')
    put(source, dest, mode=0755)
    apache_reload()


def configtest():    
    """ test Apache configuration """
    require('root', provided_by=('staging', 'production'))
    run('apachectl configtest')


def apache_reload():    
    """ reload Apache on remote host """
    require('root', provided_by=('staging', 'production'))
    run('sudo apachectl restart')


def apache_restart():    
    """ restart Apache on remote host """
    require('root', provided_by=('staging', 'production'))
    run('sudo apachectl restart')


def symlink_django():    
    """ create symbolic link so Apache can serve django admin media """
    require('root', provided_by=('staging', 'production'))
    admin_media = os.path.join(env.virtualenv_root,
                               'src/django/django/contrib/admin/media/')
    media = os.path.join(env.code_root, 'media/admin')
    if not files.exists(media):
        run('ln -s %s %s' % (admin_media, media))


def reset_local_media():
    """ Reset local media from remote host """
    require('root', provided_by=('staging', 'production'))
    media = os.path.join(env.code_root, 'media', 'upload')
    local('rsync -rvaz %s@%s:%s media/' % (env.user, env.hosts[0], media))
