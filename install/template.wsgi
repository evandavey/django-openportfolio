import os
import sys
import site

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
site_packages = os.path.join(PROJECT_ROOT, 'env/<project>/lib/python2.7/site-packages')
site.addsitedir(os.path.abspath(site_packages))
sys.path.insert(0, PROJECT_ROOT)
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
os.environ['DJANGO_SETTINGS_MODULE'] = '<project>.settings_<environment>'
os.environ['MPLCONFIGDIR'] = os.path.join(PROJECT_ROOT,'env','<project>','matplotlib')


#overcomes an issue with built in libraries being imported first
sys.path.reverse()

import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()
