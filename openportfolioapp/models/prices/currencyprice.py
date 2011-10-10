from django.db import models
from openportfolioapp.models.price import Price,PriceManager

class CurrencyPrice(Price):
	""" A listed Equity price object
	"""
	
	
	currency=models.ForeignKey("Currency")

	objects = PriceManager()
	
	class Meta:
		verbose_name_plural = "Currency Prices" #cleans up name in admin
		app_label = "openportfolioapp"
		
	
	def __unicode__(self):
		""" Returns the custom output string for this object
		"""
		return "%s - %s : %f" % (self.currency,self.date,self.price)