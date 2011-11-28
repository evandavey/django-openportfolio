from django.db import models
from openportfolioapp.models.prices.investmentprice import InvestmentPrice,InvestmentPriceManager

class SavingsAccountPrice(InvestmentPrice):
	""" A listed Equity price object
	"""
	
	
	
	class Meta:
		verbose_name_plural = "Savings Account Prices" #cleans up name in admin
		app_label = "openportfolioapp"
	
	objects = InvestmentPriceManager()
	
	
	def __unicode__(self):
		""" Returns the custom output string for this object
		"""
		return "%s - %s : %f" % (self.investment,self.date,self.price)