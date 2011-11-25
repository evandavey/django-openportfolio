from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.template.loader import render_to_string

from datetime import *
import time
from openportfolioapp.models.subclassing import SubclassingQuerySet
import pandas as ps

class InvestmentQuerySet(SubclassingQuerySet):
    """
    A queryset object that contains a date field for conversion into a pandas data frame
    """
    def datapanel(self,startdate=None,enddate=None,crosscurr=None):
        """
        Returns a panel of investment price data
        """


        qs=self
        
        if qs==[]:
            return []
        
        data={}
        for i in qs:
            
            if crosscurr is None:
                crosscurr=i.currency
            
            #need a better way, probably and investment price object
           
            data[i]=i.investmentprice_set.all().dataframe(i.currency,crosscurr)
          
        
        p=ps.Panel(data)
        
        return p

class InvestmentManager(models.Manager):
    def get_query_set(self):
        return InvestmentQuerySet(self.model)

class Investment(models.Model):
    """ A base Investment object
    Investments are issued by Companies
    Investments are held by Portfolios
    Investments are traded by Portfolios
    Investments can be Bank Accounts,Savings Accounts,Listed Equity
    Investments belong to an Asset Class
    """

    class Meta:
        verbose_name_plural = "Investments" #cleans up name in admin
        app_label = "openportfolioapp"


    name = models.CharField(max_length=255)
    company=models.ForeignKey("Company")
    asset_class=models.ForeignKey("AssetClass")
    currency=models.ForeignKey("Currency")

    """
    Subclassing code
    """
    content_type = models.ForeignKey(ContentType,editable=False,null=True)
    objects = InvestmentManager()


    def save(self, *args, **kwargs):
        if(not self.content_type):
            self.content_type = ContentType.objects.get_for_model(self.__class__)
        super(Investment, self).save(*args, **kwargs)

    def as_leaf_class(self):
        content_type = self.content_type
        model = content_type.model_class()
        if (model == Investment):
            return self
        return model.objects.get(id=self.id)

    """
    /Subclassing code
    """

	
    def __unicode__(self):
        """ Returns the custom output string for this object
        """
        return self.name

    
    def priceframe(self,startdate=None,enddate=None,crosscurr=None):
        """
        Returns a pandas dataframe containing investment prices and currency xrates
        Fields are pulled from the InvestmentPrice meta fields
        
        startdate: datetime object, defaults to all data less than enddate
        enddate: datetime object, defaults to all data greater than startdate or all data
        crosscurrency: currency object to use for cross rates, defaults to investment currency
        
        """
        if crosscurr is None:
            crosscurr=self.currency
            
        if startdate is None and enddate is None:
            df=self.investmentprice_set.all().dataframe(self.currency,crosscurr)

        elif startdate is None:
            df=self.investmentprice_set.filter(date__lte=enddate).dataframe(self.currency,crosscurr)
        elif enddate is None:
            df=self.investmentprice_set.filter(date__gte=startdate).dataframe(self.currency,crosscurr)
        else:
            df=self.investmentprice_set.filter(date__lte=enddate,date__gte=startdate).dataframe(self.currency,crosscurr)
        
      
        
        if len(df) != 0:
            df['price']=df['price'].apply(float)
            df['price_fc']=df['price']*df['xrate']
        
        return df
        
    bc_priceframe=property(priceframe) 
  
    @property
    def latest_price(self):
        
        
        try:
            p=self.investmentprice_set.all().order_by('-date')[0]
            return p.price
        except:
            return None
        
       
    
    @property
    def latest_price_date(self):

        try:
            p=self.investmentprice_set.all().order_by('-date')[0]
            return p.date
        except:
            return None


    @property
    def latest_dividend(self):

        try:
            p=self.investmentprice_set.all().order_by('-date')[0]
            return p.dividend
        except:
            return None



    @property
    def latest_dividend_date(self):

        try:
            p=self.investmentprice_set.all().order_by('-date')[0]
            return p.dividend
        except:
            return None


    @property
    def mean(self):
        """
        Returns the mean price of the investment 
        """

        df=self.bc_priceframe

        return df['price'].mean()


    def investment_chart(self):

        df=self.bc_priceframe
       
        if len(df)==0:
            return "Insufficient Pricing Data"

        lu={'data':[]}

        for dt in df.index:
            xs=df.xs(dt)
            lu['data'].append([time.mktime(dt.utctimetuple())*1000,float(xs['price'])])

        lu['name']=self.name

        return render_to_string('investment/price_chart.html', lu )

    investment_chart.allow_tags = True
    
    
    def price_table(self):

        from pandas.core.datetools import MonthEnd
        
        df=self.bc_priceframe

        if len(df)==0:
            return "Insufficient Pricing Data"
            

        df=df.asfreq(MonthEnd(),method='pad')

        df['prev_price']=df['price'].shift(1)
        
        df['capital_return']=(df['price']/df['prev_price'])-1
       
        
        lu={'prices':[]}
        
        df=df.sort(ascending=False)
        
        for dt in df.index:
            xs=df.xs(dt)
            lu['prices'].append({"date":dt,"price":xs['price'],"return":xs['capital_return']})
            
        
        lu['format']="{0:.2%}"
    

        return render_to_string('investment/price_table.html', lu )

    price_table.allow_tags = True