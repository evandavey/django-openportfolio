from django.core.management.base import BaseCommand, CommandError
from openportfolioapp.app_settings import PRICE_DOWNLOAD_DAY
from openportfolioapp.utils.update_helpers import *

from datetime import *

class Command(BaseCommand):
	args = ''
	help = 'Keeps OpenPortfolio up-to-date'

	def handle(self, *args, **options):
		
		today=datetime.today()
		
		startdate=today
		enddate=today-timedelta(days=1)
		
		
		fetch_investment_prices(startdate,enddate)
		