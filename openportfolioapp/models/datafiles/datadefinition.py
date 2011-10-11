from django.db import models
from openportfolioapp.utils.ofx import *
from openportfolioapp.models import Trade
from datetime import *
import csv

class DataDefinition(models.Model):



	class Meta:
		verbose_name_plural = "Data Definitions" #cleans up name in admin
		app_label = "openportfolioapp"
		
		
	
	""" An object to define the structure of a csv download
	"""
	investment = models.ForeignKey("Investment")
	headers = models.CharField(max_length=255)
	skip_rows = models.IntegerField(default=0)
	date_col = models.IntegerField(default=0)
	memo_col = models.IntegerField(default=-1)
	payee_col = models.IntegerField(default=-1)
	debit_col = models.IntegerField(default=-1)
	credit_col = models.IntegerField(default=-1)
	balance_col = models.IntegerField(default=-1)
	price_col = models.IntegerField(default=-1)
	cost_col = models.IntegerField(default=-1)
	date_format = models.CharField(max_length=10,default='%d/%m/%Y')
	
	def __unicode__(self):
		return str(self.investment)
