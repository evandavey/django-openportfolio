from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.db.models.query import QuerySet
import numpy

class SubclassingQuerySet(QuerySet):
    def __getitem__(self, k):
        result = super(SubclassingQuerySet, self).__getitem__(k)
        if isinstance(result, models.Model) :
            return result.as_leaf_class()
        else :
            return result
    def __iter__(self):
        for item in super(SubclassingQuerySet, self).__iter__():
            yield item.as_leaf_class()

class ReturnManager(models.Manager):
    def get_query_set(self):
        return SubclassingQuerySet(self.model)

class Return(models.Model):
	""" A base Return object
	
	""" 
	
	class Meta:
		verbose_name_plural = "Returns" #cleans up name in admin
		app_label = "openportfolioapp"
	
	FREQ_TYPES=(
		('d','Daily'),
		('m','Monthly'),
		('y','Yearly'),
	)

	date = models.DateField()
	price = models.DecimalField(decimal_places=4,max_digits=20,default=-1)
	prev_price = models.DecimalField(decimal_places=4,max_digits=20,default=-1)
	xr = models.DecimalField(decimal_places=4,max_digits=20,default=-1)
	prev_xr = models.DecimalField(decimal_places=4,max_digits=20,default=-1)
	dividend = models.DecimalField(decimal_places=4,max_digits=20,default=-1)
	freq = models.CharField(max_length=3, choices=FREQ_TYPES,blank=False)
	

	content_type = models.ForeignKey(ContentType,editable=False,null=True)
	objects = ReturnManager()

	def save(self, *args, **kwargs):
		if(not self.content_type):
			self.content_type = ContentType.objects.get_for_model(self.__class__)
			super(Return, self).save(*args, **kwargs)

	def as_leaf_class(self):
		content_type = self.content_type
		model = content_type.model_class()
		if (model == Return):
			return self
		return model.objects.get(id=self.id)
	
	def __unicode__(self):
		""" Returns the custom output string for this object
		"""
		return "%s : %f" % (self.date,self.Return)	
		

	def _capital_return(self,fc=False):
		
		p=self.price
		pp=self.prev_price
		
		if fc is True:
			p=p*self.xr
			pp=pp*self.prev_xr
		
		if numpy.isnan(float(pp)):
			return None
		
		if pp <=0:
			return None
		
		r=(p-pp)/pp
		
		return r


	def _income_return(self,fc=False):
		
		d=self.dividend
		pp=self.prev_price
		
		if fc is True:
			d=d*self.xr
			pp=pp*self.prev_xr
	
		if numpy.isnan(float(pp)) or numpy.isnan(float(d)):
			return None
		
		if pp <=0 or d <=0:
			return None
		
		r=(d)/pp
		
		return r

	def _total_return(self,fc=False):
		
		cr=self._capital_return(fc)
		ir=self._income_return(fc)
		
		if cr is None and ir is None:
			return None
			
		if cr is None:
			return ir
			
		if ir is None:
			return cr
			
		return ir+cr
		
	
	@property
	def income_return(self):
		return self._income_return()

	@property
	def income_return_fc(self):
		return self._income_return(True)
	
	@property
	def capital_return(self):
		return self._capital_return()

	@property
	def capital_return_fc(self):
		return self._capital_return(True)
	
	@property
	def total_return(self):
		return self._total_return()

	@property
	def total_return_fc(self):
		return self._total_return(True)
