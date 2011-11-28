from django.db import models
from openportfolioapp.models import Investment,InvestmentManager
from openportfolioapp.models.prices import ListedEquityPrice
from openportfolioapp.models import Trade,TradeAllocation

import matplotlib.mlab as mlab
import numpy as np
import matplotlib.finance as finance
import pandas as ps
from pandas.core.datetools import DateOffset
import sys
from datetime import *
from decimal import *


class ListedEquity(Investment):
    """ A listed Equity Investment object
    """

    class Meta:
        verbose_name_plural = "Equities" #cleans up name in admin
        app_label = "openportfolioapp"


    investment_type='ListedEquity'
    ticker = models.CharField(max_length=5)
    exchange_code = models.CharField(max_length=4,null=True,blank=True)
    objects=InvestmentManager()

    @property
    def full_ticker(self):
        """ Returns ticker.exchange_code eg: TLS.AX
        """

        if self.exchange_code:
            return self.ticker + "." + self.exchange_code
        else:
            return self.ticker


    def __unicode__(self):
        """ Returns the custom output string for this object
        """
        return self.investment_type + ":" + self.name + ":" + self.full_ticker


    def _fetch_yahoo_data(self,startdate,enddate,dividends):

        ticker=self.full_ticker


        try:
            fh = finance.fetch_historical_yahoo(ticker, startdate, enddate,None,dividends)
            # From CSV to REACARRAY
            r = mlab.csv2rec(fh); fh.close()
            # Order by Desc
            r.sort()
        except:
            print "Error: %s,%s,%s" % (sys.exc_info()[0],sys.exc_info()[1],sys.exc_info()[2])
            print "Error loading yahoo data for %s %s" % (self,str(startdate))
            return None


        return r



    def fetch_price_frame(self,startdate,enddate):

        """ Fetches price and dividend data and creates a pandas DataFrame
        of the form Date: Close,Open,High,Low,Volume,Adj_Close,Dividend
        Returns None if no data found
        """

        prices=self.fetch_prices(startdate,enddate)
        dividends=self.fetch_dividends(startdate,enddate)


        if prices is None:
            return None

        #['date','open','high','low','close','volume','adj_close']
        data={
            'close': prices.close,
            'open': prices.open,
            'high': prices.high,
            'low': prices.low,
            'volume': prices.volume,
            'adj_close': prices.adj_close,

            }

        if dividends is not None:
            divs={
                'dividend':dividends.dividends
            }

            ddf=ps.DataFrame(divs,dividends.date)
        else:
            divs={
                        'dividend':[]
            }
            ddf=ps.DataFrame(divs,[])

        #reindex dividend data to prices data
        ddf=ddf.reindex(prices.date)

        data['dividend'] = ddf['dividend']

        #create a data frame of price and dividend data
        pdf=ps.DataFrame(data,index=prices.date)

        return pdf

    def fetch_prices(self,startdate,enddate):
        """
        Returns a numpy reacarray of price data or none if no data found
        """

        return self._fetch_yahoo_data(startdate,enddate,False)


    def fetch_dividends(self,startdate,enddate):
        """
        Returns a numpy reacarray of dividend data or none if no data found
        """

        return self._fetch_yahoo_data(startdate,enddate,True)

    def save_price_frame(self,df):

        if df is None:
            return


        for dt in df.index:

            try:
                p=ListedEquityPrice.objects.get(date=dt,investment=self)
            except:
                p=ListedEquityPrice()

            xs=df.xs(dt)

            p.date=dt
            p.investment=self

            p.close=xs['close']
            p.adj_close=xs['adj_close']
            p.open=xs['open']
            if np.isnan(xs['dividend']):
                p.dividend=0
            else:
                p.dividend=xs['dividend']

            p.high=xs['high']
            p.low=xs['low']

            p.volume=xs['volume']

            p.price=p.close
            p.save()

    def price_as_at(self,date):
        p=ListedEquityPrice.objects.filter(date__lte=date,investment=self).order_by('-date')

        if len(p)==0:
            print 'Price not found for %s,%s' % (self,date)
            return None

        p=p[0]
        return p.price,p.date


    def dividend_as_at(self,date):
        p=ListedEquityPrice.objects.filter(date__lte=date,investment=self,dividend__gt=0).order_by('-date')

        if len(p)==0:
            return None

        p=p[0]
        return p.dividend,p.date



    def process_trade(self,trade):

        method='fifo'

        if trade.trade_type == 'SEL':

            if method=='fifo':
                #get buy trades for this stock ordering by earliest date for fifo
                buys=Trade.objects.filter(investment=self,trade_type='BUY',portfolio=trade.portfolio).order_by('date')
            else:
                #lifo
                buys=Trade.objects.filter(investment=self,trade_type='BUY',portfolio=trade.portfolio).order_by('-date')


            volume_allocated=0

            for b in buys:
                volume_unallocated=abs(trade.volume)-volume_allocated
                print str(volume_unallocated) + " left to allocate"
                if volume_unallocated >0:
                    try:
                        #previously used to offset sells, calc how much is left available
                        ta=TradeAllocation.objects.filter(buy_trade=b)

                        volume_available=b.volume
                        for t in ta:
                            volume_available-=t.volume

                    except ObjectDoesNotExist:
                        volume_available=b.volume

                    if volume_available > 0:
                        print "available to allocate:" + str(volume_available)

                        if volume_available>=volume_unallocated:
                            volume_to_allocate=volume_unallocated
                        else:
                            volume_to_allocate=volume_available

                        print "will allocate: " + str(volume_to_allocate)
                        ta=TradeAllocation()
                        ta.buy_trade=b
                        ta.sell_trade=trade
                        ta.volume=volume_to_allocate
                        volume_allocated+=volume_to_allocate
                        volume_unallocated-=volume_to_allocate
                        ta.save()
        return
