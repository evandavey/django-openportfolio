from django.conf.urls.defaults import *
from openportfolioapp.models import Investment,Portfolio
from django.views.generic import DetailView, ListView
from django.conf import settings


urlpatterns = patterns('',

(r'^$',
        ListView.as_view(
            queryset=Investment.objects.all,
            context_object_name='investment_list',
            template_name='openportfolioapp/index.html')),
            
            


)

"""
URLS - Admin
"""
urlpatterns += patterns('openportfolioapp.views.admin',
  (r'^admin/daily$', 
  	'daily',
  	None,
  	'daily'),
)


"""
URLS - Portfolio
"""
urlpatterns += patterns('openportfolioapp.views.portfolio',
  (r'^portfolio/(?P<portfolio_id>\d+)/report/(?:(?P<currency>\w+)/(?P<dt>\d+)/(?P<startdate>\d+)/)?$', 
  	'report',
  	None,
  	'portfolio_report'),
    

  (r'^portfolio/$',
        'list',
      	None,
      	'portfolio_list'),

)



"""
URLS - Investment
"""
urlpatterns += patterns('openportfolioapp.views.investment',

    (r'^investment/$',
      'list',
    	None,
    	'investment_list'),

  (r'^investment/(?P<investment_id>\d+)/report/(?:(?P<enddate>\d+)/(?P<startdate>\d+)/)?$',
		'report',
		None,
		'investment_report'),
)
