from django.conf.urls.defaults import patterns, include, url
from django.conf import settings

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

I18JS_URL = getattr(settings, 'I18NJS_URL', "i18njs/")

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'django_cochranedavey.views.home', name='home'),
    
	(r'^$',include('openportfolioapp.urls')),
	(r'^%s' % I18JS_URL, 'django.views.i18n.javascript_catalog'),
	
url(r'^openportfolioapp/', include('openportfolioapp.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)

"""
URLS - Accounts
"""
urlpatterns += patterns('',
 (r'^accounts/login/$', 'django.contrib.auth.views.login', {'template_name': 'login.html'}),
 (r'^accounts/logout/$', 'django.contrib.auth.views.logout',{'template_name': 'logout.html'}) 
)

if settings.DEBUG:
    urlpatterns += patterns('',
        (r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
                (r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT,}),
    )