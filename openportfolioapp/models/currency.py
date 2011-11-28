from django.db import models
from openportfolioapp.utils.currencyhistory import *
import sys
from openportfolioapp.models.prices import CurrencyPrice

class Currency(models.Model):
    code=models.CharField(max_length=6,primary_key=True)
    locale_code=models.CharField(max_length=6)

    def __unicode__(self):
        """ Returns the custom output string for this object
        """
        return self.code

    class Meta:
        verbose_name_plural = "Currencies" #cleans up name in admin
        app_label = "openportfolioapp"

    @property
    def priceframe(self):
        """
        Loads a currency queryset into a pandas dataframe
        """
        
        return self.currencyprice_set.all().dataframe()


    def fetch_price_frame(self,startdate,enddate):

        """
        Downloads data from the ukforex website, returning the result
        as a pandas dataframe
        """
        
        try:

            df = fetch_ukforex_historical_exchange_rates(startdate,enddate,self.code,'USD')

        except:
            print "Error: ", sys.exc_info()[0]
            print "Error loading uk forex data for %s %s" % (self,str(startdate))
            return None

        return df

    def save_price_frame(self,df):
        
        """
        Saves a currency dataframe object to the database
        """

        if df is None:
            return

        for dt in df.index:

            try:
                p=CurrencyPrice.objects.get(date=dt,currency=self)
            except:
                p=CurrencyPrice()

            xs=df.xs(dt)

            p.date=dt
            p.price=xs['crossrate']
            p.currency=self

            p.save()

 