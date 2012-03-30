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
        
        df=df.fillna(0)
        
    
        df['Hp']=df['portfolio'].apply(float)
        df['Hb']=df['benchmark'].apply(float)
        df['CF']=df['inflows'].apply(float)-df['outflows'].apply(float)
        df['D']=df['dividends'].apply(float)
   
        
        
        """
        Market Values
        """
        df['MV']=df['Hp']*df['P']
        df['MVb']=df['Hb']*df['P']
        df['MV_fc']=df['MV']*df['xrate']
        
        
        """
        Weights
        """
        try:
            df['Wp']=df['MV']/df['MV'].sum()
        except:
            df['Wp']=0
        
        try:
            df['Wb']=df['MVb']/df['MVb'].sum()
        except:
            df['Wb']=0
        
        df['Wa']=(df['Wp']-df['Wb'])
        
        """
        Returns
        """
        
        
        df['WRp']=df['Wp']*df['R']
        df['WRp_fc']=df['Wp']*df['R_fc']
        df['WRb']=df['Wb']*df['R']
        df['WRb_fc']=df['Wb']*df['R_fc']
        return df
    
    
    def portfolio_stats(self,panel):
        """
        Returns a dataframe of portfolio stats
        """
        
        p=panel
        
        data={'MV':[],'MVb':[],'CF':[],'D':[]}
        for dt in p.major_axis:
             df=p.major_xs(dt).T
             df=self.dataframe_calcs(df)
             data['MV'].append(df['MV'].sum())
             data['MVb'].append(df['MVb'].sum())
             data['D'].append(df['D'].sum())
             data['CF'].append(df['CF'].sum())
            

        df=ps.DataFrame(data,index=p.major_axis)
        df['PCF']=df['CF'].shift(1)
        df['PMV']=df['MV'].shift(1)
        df['PMVb']=df['MVb'].shift(1)
        
        df['R']=((df['MV']-df['CF'])/df['PMV'])-1
        
        df['Rb']=(df['MVb']/df['PMVb'])-1
        
    
        df=df.fillna(0)
        
        
        return df
      
  
    def priceframe(self,dt,crosscurr=None):
        
        if self.p is None:
            p=self.panel(dt,crosscurr=crosscurr)
            self.p=p
        else:
            p=self.p
            
        pf=self.portfolio_stats(p)
        
        return pf
        
        

    def panel(self,dt,crosscurr=None):
        
        from datetime import datetime
        bm=self.bm

        #we're dealing with a benchmark
        if bm is None:
            bm=self

        #we're going to build up holdings for transactions
        print 'Getting trades to work out unique i'
        p_trns=self.trades(dt)
        b_trns=bm.trades(dt)
        combined_trns = p_trns | b_trns
        
        #convert trades to dataframes for faster holdings calcs
        pdf=p_trns.dataframe()
        bdf=b_trns.dataframe()
        

        #unique investments in either the benchmark or portfolio
        unique_i = Investment.objects.filter(pk__in=combined_trns.values_list('investment').distinct())
        
        #creates a panel of investment data
        print "loading investment data"
        p=unique_i.datapanel(crosscurr=crosscurr)
      
        
        #hack to load holdings and create a new combined panel
        pdata={}
        print "building panel"
        for i in p.items:
            print "...%s" % i
            dates=p.major_axis
            data={'portfolio':[],'benchmark':[],'inflows':[],'outflows':[],'dividends':[]}
            
            #break out this investments dataframe of the panel
            tdf=p[i]
            
            """
            Faster holdings code - uses pandas and cumsum rather than a date loop
            """
            #portfolio holdings
            try:
                df=pdf.ix[i.id]
                df['portfolio']=df['volume'].cumsum()
            except:
                df=ps.DataFrame({'portfolio':[0]},index=[tdf.index[0]])
            
            df=df.reindex(tdf.index,method='ffill')
            
            #benchmark holdings
            try: 
                df2=bdf.ix[i.id]
                df2['benchmark']=df2['volume'].cumsum()
                
            except:
                df2=ps.DataFrame({'benchmark':[0]},index=[tdf.index[0]])
            
            df2=df2.reindex(tdf.index,method='ffill')
            
            #inflows
            inflows=p_trns.filter(investment=i,trade_type='INF').dataframe()
            
            try:
                inflows=inflows.ix[i.id]
                inflows['inflows']=inflows['volume']
            except:
                inflows=ps.DataFrame({'inflows':[0]},index=[tdf.index[0]])
            
            inflows=inflows.reindex(tdf.index)

            #outflows
            outflows=p_trns.filter(investment=i,trade_type='OUT').dataframe()

            try:
                outflows=outflows.ix[i.id]
                outflows['outflows']=outflows['volume']
            except:
                outflows=ps.DataFrame({'outflows':[0]},index=[tdf.index[0]])

            outflows=outflows.reindex(tdf.index)
        
            #dividends
            divs=p_trns.filter(investment=i,trade_type='DIV').dataframe()

            if len(divs)>0:
                divs=divs.ix[i.id]
                divs['dividends']=divs['volume']
                
            else:
                divs=ps.DataFrame({'dividends':[0]},index=[tdf.index[0]])

            divs=divs.reindex(tdf.index)
            
            
            #combine into a new dataframe
            tdf=tdf.join(df['portfolio'])
            tdf=tdf.join(df2['benchmark'])
            tdf=tdf.join(inflows['inflows'])
            tdf=tdf.join(outflows['outflows'])
            tdf=tdf.join(divs['dividends'])
            pdata[i]=tdf
        
        #reassmble the panel
        x=ps.Panel(pdata)
        
        print "Panel built"
        
        self.p=x
        
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
            p=self.panel(dt,crosscurr=crosscurr)
            self.p=p
        else:
            p=self.p
            
        
        df=self.portfolio_stats(p)
        
        if len(df)==0:
            return 0
            
        if dt is None:
            df=df.xs(df.index[-1])
        else:
            try:
                df=df.xs(dt)
            except:
                return 0
        
        return df['MV'].sum()
            
            
    @property
    def market_value(self):
    
        return self.market_value_as_at()
        
        

    """
    
    OUTPUT CODE
    
    """


    def price_chart(self,dt):

        """
        Renders a price chart vs benchmark
        """

        from pandas.core.datetools import MonthEnd

        print "building chart"


        if self.p is None:
            p=self.panel(dt,crosscurr=currency)
            self.p=p
        else:
            p=self.p

        print "....calculating stats"
        df=self.portfolio_stats(p)

        agg={
             'CF': np.sum,
             'D': np.sum,
             'R': lambda x: ((x+1).prod())-1,
             'MV': lambda x: x[0],
             'PMV': lambda x: x[0],
             'MVb': lambda x: x[0],
             'Rb': lambda x: ((x+1).prod()-1),

         }


        #Convert to monthly only for now
        df=df.groupby(lambda x: datetime(x.year,x.month,1)).agg(agg)
        
        #df=df.asfreq(MonthEnd(),method='pad')


        if len(df)==0:
            return "Insufficient pricing data"

        lu={'data':[],'bm_data':[]}

        for dt in df.index:
            xs=df.xs(dt)
            lu['data'].append([time.mktime(dt.utctimetuple())*1000,float(np.nan_to_num(xs['R'])*100)])
            lu['bm_data'].append([time.mktime(dt.utctimetuple())*1000,float(np.nan_to_num(xs['Rb'])*100)])

        lu['portfolio']=self.name
        if self.bm:
            lu['benchmark']=self.bm.name
        else:
            lu['benchmark']=self.name
            
            
        lu['name']="Portfolio vs Benchmark"

        return render_to_string('openportfolioapp/portfolio/price_chart.html', lu )

    price_chart.allow_tags = True

    def price_table(self,startdate,enddate,currency):

        """
        Renders a price table
        """

        from pandas.core.datetools import MonthEnd


        if self.p is None:
            p=self.panel(enddate,crosscurr=currency)
            self.p=p
        else:
            p=self.p


        df=self.portfolio_stats(p)
        df=df.sort()
        agg={
            'CF': np.sum,
            'D': np.sum,
            'R': lambda x: ((x+1).prod())-1,
            'MV': lambda x: x[0],
            'PMV': lambda x: x[0],
            'MVb': lambda x: x[0],
            'Rb': lambda x: ((x+1).prod()-1),

        }



        df=df.groupby(lambda x: datetime(x.year,x.month,1)).agg(agg)


        lu={'prices':[]}

        df=df.sort(ascending=False)


        if len(df)==0:
            return "Insufficient pricing data"

        for dt in df.index:
            xs=df.xs(dt)

            data={"date":dt,
                "MVp":xs['MV'],
                "PMV":xs['PMV'],
                "Rp":xs['R'],
                "MVb":xs['MVb'],
                "Rb":xs['Rb'],
                "Ra":xs['R']-xs['Rb'],
                "CF":xs['CF'],
                "D":xs['D'],
                }

            lu['prices'].append(data)


        lu['format']="{0:.2%}"


        return render_to_string('openportfolioapp/portfolio/price_table.html', lu )

    price_table.allow_tags = True


    def holdings_table(self,startdate,enddate,currency):

        #should be passed as arg


        if self.p is None:
            p=self.panel(enddate,crosscurr=currency)
            self.p=p
        else:
            p=self.p

        lu={}

        try:
            df=p.major_xs(enddate).T
            prev_df=p.major_xs(startdate).T
            df=self.dataframe_calcs(df)
            prev_df=self.dataframe_calcs(prev_df)
            
            """
            Period returns
            """
            
            df['P2']=prev_df['P']
            df['R2']=(df['P']/df['P2'])-1
            df['WR2']=df['Wp']*df['R2']
            df['WRb2']=df['Wb']*df['R2']
        
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
            {'label':'Return','key':'R2','total':None,'format':'{0:.2%}'},
            {'label':'R contrib','key':'WR2','total':None,'format':'{0:.4%}'},
            {'label':'Rb contrib','key':'WRb2','total':None,'format':'{0:.4%}'},

            ]

        lu['df']=df
        lu['report_currency']=currency


        return render_to_string('openportfolioapp/portfolio/holdings_table.html', lu )

    holdings_table.allow_tags = True


    def riskbucket_table(self,startdate,enddate,currency,bucket):
        
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
            
            """
            Period returns
            """

            df['P2']=prev_df['P']
            df['R2']=(df['P']/df['P2'])-1
            df['WR2']=df['Wp']*df['R2']
            df['WRb2']=df['Wb']*df['R2']
        
        except:
            return "Insufficient pricing data"
            
            
        group=df.groupby(bucket)
        
        data={}
        for label,gdf in group:
            data[label]={}
            data[label]["w"]=gdf['Wp'].sum()
            data[label]["wb"]=gdf['Wb'].sum()
            data[label]["rb"]=gdf['WRb2'].sum()  #just a daily return
            data[label]["mv"]=gdf['MV'].sum()
        
        group2=prev_df.groupby(bucket)

        for label,gdf2 in group2:
            data[label]["p_w"]=gdf2['Wp'].sum()
            data[label]["p_wb"]=gdf2['Wb'].sum()
            data[label]["p_mv"]=gdf2['MV'].sum()
            data[label]["p_rb"]=0.  #just a daily return
            

            
        lu['startdate']=startdate
        lu['enddate']=enddate
        lu['data']=data
        lu['format']="{0:.2%}"
        
           
        return render_to_string('openportfolioapp/portfolio/riskbucket_table.html', lu )

    riskbucket_table.allow_tags = True          
            
        

        
        
        
        