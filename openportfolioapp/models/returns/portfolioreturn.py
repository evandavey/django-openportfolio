from django.db import models
from openportfolioapp.models.returnobj import Return,ReturnManager

class PortfolioReturn(Return):
	""" An investment return object
	"""
	
	
	portfolio=models.ForeignKey("Portfolio")
	bm_price = models.DecimalField(decimal_places=4,max_digits=20,default=-1)
	bm_prev_price = models.DecimalField(decimal_places=4,max_digits=20,default=-1)
	bm_dividend = models.DecimalField(decimal_places=4,max_digits=20,default=-1)
	
	objects = ReturnManager()
	
	class Meta:
		verbose_name_plural = "Investment Returns" #cleans up name in admin
		app_label = "openportfolioapp"
		
	def __unicode__(self):
		""" Returns the custom output string for this object
		"""
		return "%s - %s : %s" % (self.portfolio,self.date,self.freq)