from django.core.management.base import BaseCommand, CommandError
from openportfolioapp.utils.update_helpers import *

from datetime import datetime

class Command(BaseCommand):
	args = '<start_date YYYYMMDD> <end_date YYYYMMDD>'
	help = 'Fetches investment prices'

	def handle(self, *args, **options):

		
		if len(args) < 2:
			raise CommandError('Requires arguments %s' % self.args)
		
	
		try:
			startdate=datetime.strptime(args[0],'%Y%m%d')
			enddate=datetime.strptime(args[1],'%Y%m%d')
		except:
			raise CommandError('Date format must be YYYYMMDD')	
		
		self.stdout.write('Fetching prices between %s and %s\n' % (startdate,enddate))
		
		fetch_investment_prices(startdate,enddate)
		fetch_currency_prices(startdate,enddate)
	