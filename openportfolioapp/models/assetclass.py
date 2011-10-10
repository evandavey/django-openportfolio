from django.db import models
from openportfolioapp.utils import full_name

class AssetClass(models.Model):
	""" An object to represent an investment AssetClass
		Each Investment will belong to a single AssetClass
	"""

	class Meta:
		verbose_name_plural = "Asset classes" #cleans up name in admin
		app_label = "openportfolioapp"

	name = models.CharField(max_length=255)
	parent = models.ForeignKey('self',blank=True,null=True,related_name='child')
	benchmark = models.ForeignKey("Portfolio")	
	
	def _full_name(self):
		return full_name(self)
		
	full_name=property(_full_name)
		
	def __unicode__(self):
		""" Returns the custom output string for this object
		"""
		return self.full_name
		
