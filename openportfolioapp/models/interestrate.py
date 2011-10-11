from django.db import models


class InterestRate(models.Model):
	""" 
	""" 
	
	class Meta:
		verbose_name_plural = "Interest Rates" #cleans up name in admin
		app_label = "openportfolioapp"


	investment=models.ForeignKey("Investment")
	date = models.DateField()
	annualrate=models.DecimalField(decimal_places=4,max_digits=20,default=-1)
	
	
	
	