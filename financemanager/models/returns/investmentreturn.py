from django.db import models
from financemanager.models.returnobj import Return,ReturnManager

class InvestmentReturn(Return):
	""" An investment return object
	"""
	
	
	investment=models.ForeignKey("Investment")

	objects = ReturnManager()
	
	class Meta:
		verbose_name_plural = "Investment Returns" #cleans up name in admin
		app_label = "financemanager"
		
	def __unicode__(self):
		""" Returns the custom output string for this object
		"""
		return "%s - %s : %f" % (self.investment,self.date,self.total_return)