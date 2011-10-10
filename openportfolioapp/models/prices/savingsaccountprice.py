from django.db import models
from financemanager.models.price import Price,PriceManager

class SavingsAccountPrice(Price):
	""" A listed Equity price object
	"""
	
	investment=models.ForeignKey("Investment")
	dividend=models.DecimalField(decimal_places=10,max_digits=20,default=-1)
	
	class Meta:
		verbose_name_plural = "Savings Account Prices" #cleans up name in admin
		app_label = "financemanager"
	
	objects = PriceManager()
	
	
	def __unicode__(self):
		""" Returns the custom output string for this object
		"""
		return "%s - %s : %f" % (self.investment,self.date,self.price)