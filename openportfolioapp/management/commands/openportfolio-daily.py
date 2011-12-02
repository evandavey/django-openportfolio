from django.core.management.base import BaseCommand, CommandError
from openportfolioapp.utils.update_helpers import *

from datetime import *

class Command(BaseCommand):
	args = ''
	help = 'Keeps OpenPortfolio up-to-date'

	def handle(self, *args, **options):
		
		today=datetime.today()
		
		
		enddate=today-timedelta(days=1)
		startdate=enddate-timedelta(days=5)
		
		fetch_investment_prices(startdate,enddate)
		fetch_currency_prices(startdate,enddate)