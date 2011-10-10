from django.db import models
from openportfolioapp.models.price import Price,PriceManager

class PortfolioPrice(Price):
	""" A listed Equity price object
	"""
	
	portfolio=models.ForeignKey("Portfolio")
	marketvalue=models.DecimalField(decimal_places=4,max_digits=20,default=-1)
	numholdings=models.IntegerField(default=-1)
	
	
	class Meta:
		verbose_name_plural = "Portfolio Prices" #cleans up name in admin
		app_label = "openportfolioapp"
	
	objects = PriceManager()
	
	
	def __unicode__(self):
		""" Returns the custom output string for this object
		"""
		return "%s - %s : %f" % (self.portfolio,self.date,self.price)