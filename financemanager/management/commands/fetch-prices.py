from django.core.management.base import BaseCommand, CommandError
from financemanager.models import Investment
from financemanager.models import Currency

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
		
	
		self.stdout.write('.Fetching investment prices\n')
		for i in Investment.objects.all():
		
			pdf=i.fetch_price_frame(startdate,enddate)
			
			
			if pdf is not None:
				i.save_price_frame(pdf)
				self.stdout.write('..successfully fetched prices for "%s"\n' % i)
			
			pdf=None

		self.stdout.write('.Fetching currency prices\n')
		for c in Currency.objects.all():
			pdf=c.fetch_price_frame(startdate,enddate)
			
			#print pdf
			if pdf is not None:
				c.save_price_frame(pdf)
				self.stdout.write('..successfully fetched prices for "%s"\n' % c)
			
			pdf=None
