from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.db.models.query import QuerySet

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

class PriceManager(models.Manager):
    def get_query_set(self):
        return SubclassingQuerySet(self.model)

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
		
