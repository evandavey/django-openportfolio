from django.db import models

class Company(models.Model):
	""" A high level object to represent a company 
		Companies can issue multiple Investments
	"""
	
	class Meta:
		verbose_name_plural = "Companies" #cleans up name in admin
		app_label = "openportfolioapp"
		
	
	name = models.CharField(max_length=255)
	gics_sector = models.ForeignKey("GICSSector")

	def __unicode__(self):
		""" Returns the custom output string for this object
		"""
		return self.name
		