#!/bin/sh
source /usr/local/web/django/www/production/env/openportfolio/bin/activate
/usr/local/web/django/www/production/openportfolio/manage.py openportfolio-update --settings=openportfolio.settings_production
