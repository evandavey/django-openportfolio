from django.db import models
from django.contrib.contenttypes.models import ContentType

from openportfolioapp.models.price import Price,PriceManager,PriceQuerySet
import pandas as ps

DEFAULT_CURRENCY='AUD'

class InvestmentPriceQuerySet(PriceQuerySet):
    """
    A queryset object that contains a date field for conversion into a pandas data frame
    """



    def dataframe(self,basecurrency,crosscurrency):


        df=super(InvestmentPriceQuerySet,self).dataframe()

        if not df:
            return None

        base_df=basecurrency.priceframe
        cross_df=crosscurrency.priceframe

        currdata={'base_currency':base_df.reindex(df.index,method='ffill')['price'],
        'cross_currency':cross_df.reindex(df.index,method='ffill')['price']
        }

        curr_df=ps.DataFrame(currdata,index=df.index)

        curr_df=curr_df.applymap(float)
        curr_df['xrate']=curr_df['base_currency']/curr_df['cross_currency']

        df=df.join(curr_df['xrate'])
    
        
        return df

class InvestmentPriceManager(models.Manager):
    def get_query_set(self):
        return InvestmentPriceQuerySet(self.model)


class InvestmentPrice(Price):
    """ A listed Equity price object
    """

    investment=models.ForeignKey("Investment")
    dividend=models.DecimalField(decimal_places=10,max_digits=20,default=-1)


    objects = InvestmentPriceManager()

    class Meta:
        verbose_name_plural = "Investment Prices" #cleans up name in admin
        app_label = "openportfolioapp"


    def as_leaf_class(self):
        content_type = self.content_type
        model = content_type.model_class()
        if (model == InvestmentPrice):
            return self
        return model.objects.get(id=self.id)

    def __unicode__(self):
        """ Returns the custom output string for this object
        """
        return "%s - %s : %f" % (self.investment,self.date,self.price)
