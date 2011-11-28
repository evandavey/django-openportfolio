from django.db import models
from openportfolioapp.models.prices.investmentprice import InvestmentPrice,InvestmentPriceManager

class ListedEquityPrice(InvestmentPrice):
	""" A listed Equity price object
	"""
	
	close=models.DecimalField(decimal_places=4,max_digits=20,default=-1)
	adj_close=models.DecimalField(decimal_places=4,max_digits=20,default=-1)
	high=models.DecimalField(decimal_places=4,max_digits=20,default=-1)
	low=models.DecimalField(decimal_places=4,max_digits=20,default=-1)
	open=models.DecimalField(decimal_places=4,max_digits=20,default=-1)
	volume=models.DecimalField(decimal_places=0,max_digits=20,default=-1)
	
	objects = InvestmentPriceManager()
	
	class Meta:
		verbose_name_plural = "Equities Prices" #cleans up name in admin
		app_label = "openportfolioapp"
		
	
	def __unicode__(self):
		""" Returns the custom output string for this object
		"""
		return "%s - %s : %f" % (self.investment,self.date,self.price)