from openportfolioapp.models import Investment
from openportfolioapp.models import Currency
from openportfolioapp.models import Portfolio

def fetch_investment_prices(startdate,enddate):
	
	print 'updating prices between %s-%s' % (startdate,enddate)
	for i in Investment.objects.all():
	
		pdf=i.fetch_price_frame(startdate,enddate)
			
		if pdf is not None:
			i.save_price_frame(pdf)
		
		pdf=None

def fetch_currency_prices(startdate,enddate):

	for c in Currency.objects.all():
		pdf=c.fetch_price_frame(startdate,enddate)
		
		if pdf is not None:
			c.save_price_frame(pdf)
		
		pdf=None

def update_portfolio_prices(startdate,endate):
	
	for p in Portfolio.objects.all():
	
		pdf=p.load_holdings_frame(startdate,enddate)
		
		if pdf is not None:
			p.save_holdings_frame(pdf)
		
		pdf=None

	