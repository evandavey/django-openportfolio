#Open Portfolio

Open source django project for portfolio management.  Aims to open up asset management tools used by professional fund managers.

More information at: [project homepage](http://evandavey.github.io/django-openportfolio/)


# License

[Creative Commons Share Alike Non-Commercial](http://creativecommons.org/licenses/by-nc-sa/2.0/uk/deed.en_GB)

#Change History

v0.1:

* implements basic functionality
	- create / edit objects through the django admin interface
	- trades can be uploaded as csv or ofx
	- portfolios can be grouped and assigned benchmarks
	- handles investments and reporting in cross currencies
	- management command to download prices, can be run as a scheduled task
	- Highcharts price charts for portfolios and investments
	- benchmark relative portfolio report showing holdings and returns over time
	- investment report showing price chart and other pricing data
	- pandas dataframes and panels used in backend giving substantial flexibility for future reporting enhancements (such as risk calculations, risk weighting analysis, gips compliant returns calcs...)
	- fifo / lifo trade allocations for profit calculations
	
	
	


#Installation

See [installation](http://evandavey.github.io/django-openportfolio/installation.html)

#Project documentation 

See [project docs](http://evandavey.github.io/django-openportfolio/)


#Author

Evan Davey, evan.j.davey@gmail.com, www.twitter.com/evanjdavey/

