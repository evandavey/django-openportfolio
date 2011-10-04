## modified matplotlib.finance.fetch_historical_yahoo
import datetime
import os, warnings
from urllib2 import urlopen

try:
    from hashlib import md5
except ImportError:
    from md5 import md5 #Deprecated in 2.5
import datetime

from matplotlib import verbose, get_configdir
from matplotlib.cbook import iterable

configdir = get_configdir()
cachedir = os.path.join(configdir, 'finance.cache')


def my_fetch_historical_yahoo(ticker, date1, date2, cachename=None,dividends=False):
    """
    Fetch historical data for ticker between date1 and date2.  date1 and
    date2 are date or datetime instances, or (year, month, day) sequences.

    Ex:
    fh = fetch_historical_yahoo('^GSPC', (2000, 1, 1), (2001, 12, 31))

    cachename is the name of the local file cache.  If None, will
    default to the md5 hash or the url (which incorporates the ticker
    and date range)

    a file handle is returned
    """

	
    ticker = ticker.upper()


    if iterable(date1):
        d1 = (date1[1]-1, date1[2], date1[0])
    else:
        d1 = (date1.month-1, date1.day, date1.year)
    if iterable(date2):
        d2 = (date2[1]-1, date2[2], date2[0])
    else:
        d2 = (date2.month-1, date2.day, date2.year)


	if dividends:
		g='v'
	else:
		g='d'

    urlFmt = 'http://table.finance.yahoo.com/table.csv?a=%d&b=%d&c=%d&d=%d&e=%d&f=%d&s=%s&y=0&g=%s&ignore=.csv'


    url =  urlFmt % (d1[0], d1[1], d1[2],
                     d2[0], d2[1], d2[2], ticker,g)

    print url

    if cachename is None:
        cachename = os.path.join(cachedir, md5(url).hexdigest())
    if os.path.exists(cachename):
        fh = file(cachename)
        verbose.report('Using cachefile %s for %s'%(cachename, ticker))
    else:
        if not os.path.isdir(cachedir):
            os.mkdir(cachedir)
        urlfh = urlopen(url)

        fh = file(cachename, 'w')
        fh.write(urlfh.read())
        fh.close()
        verbose.report('Saved %s data to cache file %s'%(ticker, cachename))
        fh = file(cachename, 'r')

    return fh


	

