from django.db import models
from django.contrib.contenttypes.models import ContentType
from openportfolioapp.models.subclassing import SubclassingQuerySet
import pandas as ps
import numpy as np


class PriceQuerySet(SubclassingQuerySet):
    """
    A queryset object that contains a date field for conversion into a pandas data frame
    """
    def dataframe(self):
        
        qs=self
        
        if len(qs)==0:
            return None

        dates=list(qs.dates('date','day'))
        
        vlqs = qs.values_list()
        r = np.core.records.fromrecords(vlqs, names=[f.name for f in self.model._meta.fields])
        
        df=ps.DataFrame(r,index=dates)
        
        return df

class PriceManager(models.Manager):
    def get_query_set(self):
        return PriceQuerySet(self.model)


class Price(models.Model):
	""" A base Price object
	
	""" 
	
	class Meta:
		verbose_name_plural = "Prices" #cleans up name in admin
		app_label = "openportfolioapp"
	

	date = models.DateField()
	price=models.DecimalField(decimal_places=4,max_digits=20,default=-1)
	
	content_type = models.ForeignKey(ContentType,editable=False,null=True)
	objects = PriceManager()

	def save(self, *args, **kwargs):
		if(not self.content_type):
			self.content_type = ContentType.objects.get_for_model(self.__class__)
			super(Price, self).save(*args, **kwargs)

	def as_leaf_class(self):
		content_type = self.content_type
		model = content_type.model_class()
		if (model == Price):
			return self
		return model.objects.get(id=self.id)
	
	def __unicode__(self):
		""" Returns the custom output string for this object
		"""
		return "%s : %f" % (self.date,self.price)	
		
