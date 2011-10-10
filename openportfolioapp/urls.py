from django.conf.urls.defaults import *
from financemanager.models import Investment,Portfolio
from django.views.generic import DetailView, ListView
from django.conf import settings


urlpatterns = patterns('',

(r'^$',
        ListView.as_view(
            queryset=Investment.objects.all,
            context_object_name='investment_list',
            template_name='financemanager/index.html')),

(r'^investment/$',
        ListView.as_view(
            queryset=Investment.objects.all,
            context_object_name='investment_list',
            template_name='financemanager/investment_list.html')),


(r'^portfolio/$',
       ListView.as_view(
            queryset=Portfolio.objects.all,
            context_object_name='portfolio_list',
            template_name='financemanager/portfolio_list.html')),


(r'^portfolio/(?P<portfolio_id>\d+)/report/(?:(?P<currency>\w+)/(?P<dt>\d+)/)?$', 
	'financemanager.views.portfolio_report',
	None,
	'portfolio_report'),


(r'^portfolio/(?P<portfolio_id>\d+)/report/(?:(?P<currency>\w+)/(?P<dt>\d+)/)?barchart.png/(?P<analysis_field>\w+)/$',
	'financemanager.views.portfolio_barchart',
	None,
	'portfolio_barchart'),

(r'^investment/(?P<investment_id>\d+)/report/(?:(?P<enddate>\d+)/(?P<startdate>\d+)/)?$',
		'financemanager.views.investment_report',
		None,
		'investment_report'),

(r'^investment/(?P<investment_id>\d+)/report/(?:(?P<enddate>\d+)/(?P<startdate>\d+)/)?investmentchart.png/$',
	'financemanager.views.investment_chart',
	None,
	'investment_chart'),

(r'^test/$', 
	'financemanager.views.returns_table',
	None,
	'returns_table'),

)