#Open Financial Management

Open source django project for portfolio management.  Aims to open up asset management tools used by professional fund managers.

* Manage portfolios of investments

* Cross currency capabilities

* Reporting of portfolio characteristics
	* Returns (aims to be GIPS compliant)
	* Weighting by asset class, sectors, companies...
	* Cash flows (aims to allow for after-tax reporting)
	* Trade history (including profit & loss)
	* Risk factor modelling
	
* Analysis of investments
	* Return and risk characteristics
	* Performance plots including technical trade indicators

* Benchmark relative reporting for performance and risk analysis 
	* Benchmarks can be arbitrary portfolios

* Utilises online price feeds where available

* Can use scheduled commands for automatic price downloads, return calculations

* Matplotlib utilised for portfolio reporting charts


#Install

The easy option is to install fabric and utitilse the included fabfile.  A virtual environment is recommended.

Otherwise:

- install requirements
    pip install -e requirements/apps.txt

- sync the database
    pip ./manage.py syncdb --settings=financedb.settings_local

- run the development server
	pip ./manage.py runserver 0.0.0.0:8080 --settings=financedb.settings_local
	
	
The fabfile includes scripts to deploy within a production environment using Apache2 and Passenger.


 
#Dependencies
* pip
* virtualenv
* virtualenvwrapper
* fabric

* django
* numpy
* matplotlib
* pandas
* BeautifulSoup

* pyYAML
* mysql-python

#Author

Evan Davey, evan.j.davey@gmail.com, www.twitter.com/evanjdavey/

*** PRE RELEASE ***
