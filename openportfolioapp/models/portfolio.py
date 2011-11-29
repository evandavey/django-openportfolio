from django.db import models
from django.template.loader import render_to_string

import pandas as ps
import numpy as np
from datetime import *
from decimal import *
import time

from openportfolioapp.utils import full_name
from openportfolioapp.models.trade import Trade
from openportfolioapp.models.investment import Investment
from pandas.core.datetools import DateOffset,MonthEnd,YearEnd



DEFAULT_CURRENCY='AUD'

class Portfolio(models.Model):

    """ A portfolio object
    """

    class Meta:
        app_label = "openportfolioapp"

    name = models.CharField(max_length=255)
    parent = models.ForeignKey('self',blank=True,null=True,related_name='child')
    bm=models.ForeignKey('self',null=True,related_name='benchmark',blank=True)

    def _full_name(self):
        return full_name(self)

    full_name=property(_full_name)

    def __unicode__(self):
        """ Returns the custom output string for this object
        """
        return self.full_name

   
    p=None  #cache variable for the data panel
    
    def dataframe_calcs(self,df):
        """
        Performs portfolio calculations on a dataframe.
        Ideally this would be instead done on the portfolio panel.
        """
        
        """
        Price & Holdings
        """
        df['P']=df['price'].apply(float)
        df['P_fc']=df['P']*df['xrate']
        df['Hp']=df['portfolio']
        df['Hb']=df['benchmark']
        
        """
        Weights
        """
        try:
            df['Wp']=df['Hp']/df['Hp'].sum()
        except:
            df['Wp']=0
        
        try:
            df['Wb']=df['Hb']/df['Hb'].sum()
        except:
            df['Wb']=0
        
        df['Wa']=df['Wp']-df['Wb']
        
        """
        Market Values
        """
        df['MV']=df['Hp']*df['P']
        df['MVb']=df['Hb']*df['P']
        df['MV_fc']=df['MV']*df['xrate']
        
        
        
        return df
    
    
    def portfolio_stats(self,panel):
        """
        Returns a dataframe of portfolio stats
        """
        
        p=panel
        
        data={'MV':[],'MVb':[]}
        for dt in p.major_axis:
             df=p.major_xs(dt).T
             df=self.dataframe_calcs(df)
             data['MV'].append(df['MV'].sum())
             data['MVb'].append(df['MVb'].sum())

        df=ps.DataFrame(data,index=p.major_axis)
        
        return df

    def price_chart(self):
        
        """
        Renders a price chart vs benchmark
        """

        from pandas.core.datetools import MonthEnd


        if self.p is None:
            p=self.panel(crosscurr=currency)
            self.p=p
        else:
            p=self.p
            

        df=self.portfolio_stats(p)
       
        #Convert to monthly only for now
        df=df.asfreq(MonthEnd(),method='pad')
        
        df['MV2']=df['MV'].shift(1)
        df['MV2b']=df['MVb'].shift(1)
        
        df['Rp']=(df['MV']/df['MV2'])-1
        df['Rb']=(df['MVb']/df['MV2b'])-1
        
        
        
        
        if len(df)==0:
            return "Insufficient pricing data"

        lu={'data':[],'bm_data':[]}

        for dt in df.index:
            xs=df.xs(dt)
            lu['data'].append([time.mktime(dt.utctimetuple())*1000,float(np.nan_to_num(xs['Rp'])*100)])
            lu['bm_data'].append([time.mktime(dt.utctimetuple())*1000,float(np.nan_to_num(xs['Rb'])*100)])
        
        lu['portfolio']=self.name
        lu['benchmark']=self.bm.name
        lu['name']="Portfolio vs Benchmark"

        return render_to_string('portfolio/price_chart.html', lu )

    price_chart.allow_tags = True
   
    def price_table(self,startdate,enddate,currency):
        
        """
        Renders a price table
        """
        
        from pandas.core.datetools import MonthEnd


        if self.p is None:
            p=self.panel(crosscurr=currency)
            self.p=p
        else:
            p=self.p
            

        df=self.portfolio_stats(p)
       
        #Convert to monthly only for now
        df=df.asfreq(MonthEnd(),method='pad')
        
        #Returns calcs (will need to adjust for cash flows)
        df['MV2']=df['MV'].shift(1)
        df['Rp']=(df['MV']/df['MV2'])-1
       
        df['MVb2']=df['MVb'].shift(1)
        df['Rb']=(df['MVb']/df['MVb2'])-1
        
        lu={'prices':[]}
        
        df=df.sort(ascending=False)
        
        
        if len(df)==0:
            return "Insufficient pricing data"
        
        for dt in df.index:
            xs=df.xs(dt)
            
            data={"date":dt,
                "MVp":xs['MV'],
                "Rp":xs['Rp'],
                "MVb":xs['MVb'],
                "Rb":xs['Rb'],
                "Ra":xs['Rp']-xs['Rb'],
                }
            
            lu['prices'].append(data)
             

        lu['format']="{0:.2%}"


        return render_to_string('portfolio/price_table.html', lu )

    price_table.allow_tags = True
    
    
    def holdings_table(self,startdate,enddate,currency):

        #should be passed as arg
        

        if self.p is None:
            p=self.panel(crosscurr=currency)
            self.p=p
        else:
            p=self.p
        
        lu={}

        try:
            df=p.major_xs(enddate).T
            prev_df=p.major_xs(startdate).T
            df=self.dataframe_calcs(df)
            prev_df=self.dataframe_calcs(prev_df)
            df['P2']=prev_df['P']
        except:
            return "Insufficient pricing data"
        
        lu['fields']=[
            {'label':'Hp','key':'Hp','total':'sum','format':'{0:.2f}'},
            {'label':'Wp','key':'Wp','total':'sum','format':'{0:.2%}'},
            {'label':'Wa','key':'Wa','total':'sum','format':'{0:.2%}'},
            {'label':'Market Value','key':'MV_fc','total':'sum','format':'rc'},
            {'label':'Market Value','key':'MV','total':None,'format':'lc'},
            {'label':'Price','key':'P','total':None,'format':'lc'},
            {'label':'Price','key':'P_fc','total':None,'format':'rc'},
            {'label':'Prev Price','key':'P2','total':None,'format':'lc'},
            ]
			
        lu['df']=df
        lu['report_currency']=currency
        

        return render_to_string('portfolio/holdings_table.html', lu )

    holdings_table.allow_tags = True

    def panel(self,crosscurr=None):
        
        from datetime import datetime
        dt=datetime(2011,10,31)
        bm=self.bm

        #we're dealing with a benchmark
        if bm is None:
            bm=self

        #we're going to build up holdings for transactions
        p_trns=self.trades(dt)
        b_trns=bm.trades(dt)
        combined_trns = p_trns | b_trns

        #unique investments in either the benchmark or portfolio
        unique_i = Investment.objects.filter(pk__in=combined_trns.values_list('investment').distinct())
        
        #creates a panel of investment data
        p=unique_i.datapanel(crosscurr=crosscurr)
        from django.db.models import Sum
        
        #hack to load holdings and create a new combined panel
        pdata={}
        print "building panel"
        for i in p.items:
            print "...%s" % i
            dates=p.major_axis
            data={'portfolio':[],'benchmark':[]}
            for dt in dates:
                p_trns=self.trades(dt)
                b_trns=bm.trades(dt)
                ph=p_trns.filter(investment=i).aggregate(Sum('volume'))['volume__sum']
                bh=b_trns.filter(investment=i).aggregate(Sum('volume'))['volume__sum']
                
                if ph is None:
                    ph=0
                    
                if bh is None:
                    bh=0
                
                data['portfolio'].append(ph)
                data['benchmark'].append(bh)
        
        
            df=ps.DataFrame(data,index=dates)
            df=df.applymap(float)
            tdf=p[i]
            #tdf['price']=tdf['price'].applymap(float)
        
            tdf=tdf.join(df['portfolio'])
            tdf=tdf.join(df['benchmark'])
            pdata[i]=tdf
        
        x=ps.Panel(pdata)
        
        return x

    
    def trades(self,dt,startdate=None,trade_type=None):
        
        """
        Loads all trades for that people and its children
        """

        if startdate is None:
            trns=Trade.objects.filter(date__lte=dt,portfolio=self)
        else:
            trns=Trade.objects.filter(date__lte=dt,date__gte=startdate,portfolio=self)

        if trade_type is not None:
            trns=trns.filter(trade_type=trade_type)

        for c in self.child.all():
            trns = trns | c.trades(dt,startdate,trade_type)

        return trns

 
    def market_value_as_at(self,dt=None,crosscurr=None):
        
        if self.p is None:
            p=self.panel(crosscurr=crosscurr)
            self.p=p
        else:
            p=self.p
            
        
        df=self.portfolio_stats(p)
        
        if len(df)==0:
            return 0
            
        if dt is None:
            df=df.xs(df.index[-1])
        else:
            df=df.xs(dt)
        
        return df['MV'].sum()
            
            
    @property
    def market_value(self):
    
        return self.market_value_as_at()
       