from django.core.management.base import BaseCommand, CommandError
from financemanager.models import Portfolio

from pandas.core.datetools import MonthEnd
from datetime import datetime

class Command(BaseCommand):
	args = '<start_date YYYYMMDD> <end_date YYYYMMDD>'
	help = 'Fetches porfolio prices'

	def handle(self, *args, **options):
		
		if len(args) < 2:
			
			enddate=datetime.today()-MonthEnd()
			startdate=enddate-MonthEnd()
		else:	
			try:
				startdate=datetime.strptime(args[0],'%Y%m%d')
				enddate=datetime.strptime(args[1],'%Y%m%d')
			except:
				raise CommandError('Date format must be YYYYMMDD')	
		
	
		
		self.stdout.write('Fetching prices between %s and %s\n' % (startdate,enddate))
		
	
		self.stdout.write('.Fetching portfolio prices\n')
		for p in Portfolio.objects.all():
		
			self.stdout.write('..%s\n' % p)
			pdf=p.load_holdings_frame(startdate,enddate)
			
			
			if pdf is not None:
				p.save_holdings_frame(pdf)
				self.stdout.write('..successfully saved portfolio prices for "%s"\n' % p)
			
			pdf=None

