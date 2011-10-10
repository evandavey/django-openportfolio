from django.db import models
from openportfolioapp.utils import full_name

class GICSSector(models.Model):
	""" An object to represent the S&P GICS sector structure
		Each Company will belong to a single GICS sector
		The GICS sectors hieracy defines levels of Sector,IndustryGroup,Industry and SubIndustry
		GICS data will be populated from a (manipulated) csv file downloaded from S&P
		Note that the ASX company data populates GICS sectors at the IndustryGroup level 
		S&P use an id scheme that allows the parent/child relationship to be determined from the id
		For example, an Industry of id 102030 will belong to IndustryGroup id 1020 and Sector 10
	"""

	class Meta:
		verbose_name_plural = "GICS Sectors" #cleans up name in admin
		app_label = "openportfolioapp"
        
		

	GICS_LEVELS=(
		('Industry','Industry'),
		('SubIndustry','Sub-Industry'),
		('IndustryGroup','Industry-Group'),
		('Sector','Sector'),

	)

	code=models.CharField(max_length=8,primary_key=True) #The S&P id scheme, SubIndustries have at most 8 characters
	name = models.CharField(max_length=255)
	description=models.TextField(blank=True) #Available for subindustry only
	level = models.CharField(max_length=13,choices=GICS_LEVELS,blank=False)
	parent = models.ForeignKey('self',blank=True,null=True,related_name='child')	

	def _full_name(self):
		return full_name(self)
		
	full_name=property(_full_name)

	def __unicode__(self):
		""" Returns the custom output string for this object
		"""
		return self.full_name

	def _get_sector(self):
		""" Gets the linked Sector level name
		"""

		if self.level=='SubIndustry':
			return self.parent.parent.parent.name
		elif self.level=='Industry':
			return self.parent.parent.name
		elif self.level=='IndustryGroup':
			return self.parent.name
		else:
			return self.name


	sector = property(_get_sector)

	def _get_industry_group(self):
		""" Gets the linked Industry Group level name
		"""

		if self.level=='SubIndustry':
			return self.parent.parent.name
		elif self.level=='Industry':
			return self.parent.name
		elif self.level=='IndustryGroup':
			return self.name
		else:
			return 'Not Available'

	industry_group = property(_get_industry_group)

	def _get_industry(self):
		""" Gets the linked Industry level name
		"""

		if self.level=='SubIndustry':
			return self.parent.name
		elif self.level=='Industry':
			return self.name
		else:
			return 'Not Available'

	industry = property(_get_industry)
