from django.db import models
from openportfolioapp.utils.ofx import *
from openportfolioapp.models import Trade,Portfolio,ListedEquity
from openportfolioapp.models.datafiles import DataDefinition
from datetime import *
import csv

class TradeDataFile(models.Model):
	""" An object to represent a download file of Trades
		1 file per portfolio
	"""


	class Meta:
		verbose_name_plural = "Trade Data Files" #cleans up name in admin
		app_label = "openportfolioapp"
		
		
	start_date = models.DateField(editable=False) #set from file
	end_date = models.DateField(editable=False) #set from file
	file_name = models.FileField(upload_to='datafiles/trades')

	investment=models.ForeignKey("Investment",blank=True,null=True)
	portfolio=models.ForeignKey("Portfolio",blank=True,null=True)
	transactions=models.ManyToManyField("Trade",editable=False)
	bulkfile=models.BooleanField(default=False)

	data=[]



	def _load_data_csv(self):
		reader=csv.reader(self.file_name)

		if self.bulkfile:
			#"Date","Portfolio","Stock_Code","Units","Price","Cost","Type","Description"
			
			datadef=DataDefinition()
			datadef.date_col=0
			datadef.date_format="%Y%m%d"
			datadef.credit_col=3
			datadef.price_col=4
			datadef.cost_col=5
			datadef.memo_col=7
			datadef.investment_col=2
			datadef.portfolio_col=1		
			
		else:
			datadef=DataDefinition.objects.get(investment=self.investment)
	
		if datadef is None:
			return False

		for i in range(0,datadef.skip_rows):
			junk=reader.next()
		
		header=reader.next()
	
	
		self.data=[]
	
		row_i=0
		for row in reader:
		
			row_i+=row_i
			if row==[]:
				pass
			else:
		
				date_format=datadef.date_format
				dt=str(row[datadef.date_col])
				#print 'Date is:' +dt
				dt=datetime.strptime(dt,str(date_format))
		
				if datadef.payee_col == -1:
					payee=""
				else:
					#print 'Payee:' + row[datadef.payee_col]
					payee=str(row[datadef.payee_col])
			
				if datadef.memo_col == -1:
					memo=""
				else:
					memo=row[datadef.memo_col]
			
			
				if datadef.debit_col == -1:
					debit=0
				else:
			
					debit=str(row[datadef.debit_col]).replace("$","").replace(",","")
			
					if debit=="":
						debit=0
					else:
						debit=abs(float(debit))
			
			
				if datadef.credit_col == -1:
					credit=0
				else:
			
					credit=str(row[datadef.credit_col]).replace("$","").replace(",","")
			
					if credit=="":
						credit=0
					else:
						credit=abs(float(credit))
			
			
				amount=credit-debit
		
				myid=None
				
				if datadef.price_col == -1:
					price=1.0
				else:
					price=float(row[datadef.price_col])
						
				
				if datadef.cost_col == -1:
					cost=0.0
				else:
					cost=float(row[datadef.cost_col])
				
				
				if self.bulkfile:
					
					portfolio_id=str(row[datadef.portfolio_col])
					investment_id=str(row[datadef.investment_col])
					
					ticker=investment_id.split('.')
					
					
					try:
						portfolio=Portfolio.objects.get(name=portfolio_id)
						investment=ListedEquity.objects.get(ticker=ticker[0],exchange_code=ticker[1])
						
					except:
						import sys
						print "Unexpected error:", sys.exc_info()[0]
						print "Error reading bulk file: %s-%s" % (portfolio_id,investment_id)
						continue
						
					
					
					
				else:	
					investment=self.investment
					portfolio=self.portfolio
		
				self.data.append({
					"date":dt,
					"memo":memo,
					"payee":payee,
					"amount":amount,
					"transid":myid,
					"cost":cost,
					"price":price,
					"portfolio": portfolio,
					"investment": investment,
					})

	def _load_data_ofx(self):
	
		""" Function to populate the data[] variable by loading an ofx file
		"""
		
	    
		ofx = OfxParser.parse(self.file_name)


		self.data=[]
		bankid=clean_ofx_str(ofx.bank_account.routing_number)
		accid=clean_ofx_str(ofx.bank_account.number)


		for t in ofx.bank_account.statement.transactions:
			amount=float(t.amount)
			payee=clean_ofx_str(t.payee)
			memo=clean_ofx_str(t.memo)
			dt=parse_ofx_date(clean_ofx_str(t.date))
			myid=clean_ofx_str(t.id)
			price=1.0
			cost=0.0
	
			investment=self.investment
			portfolio=self.portfolio
	
			self.data.append({
				"date":dt,
				"memo":memo,
				"payee":payee,
				"amount":amount,
				"transid":myid,
				"cost":cost,
				"price":price,
				"portfolio": portfolio,
				"investment": investment,
				})
		return True

	def _set_dates_from_data(self):
	
		""" Function to set the date range from the data file
		"""

		start_dt=None
		end_dt=None

		for d in self.data:


			dt=d['date']

			if start_dt is None:
				start_dt=dt
			else:
				if dt < start_dt:
					start_dt=dt

			if end_dt is None:
				end_dt=dt
			else:
				if dt > end_dt:
					end_dt=dt

		self.start_date=start_dt
		self.end_date=end_dt


	def _create_transactions_from_data(self):
		""" Function to create transactions from data[]
		"""


		#delete old transactions in this date range
		self.transactions.all().delete()
		Trade.objects.filter(date__lte=self.end_date,date__gte=self.start_date,investment=self.investment,portfolio=self.portfolio).delete()

		for d in self.data:
		
			#print 'creating a trans...'
	
			t=Trade()


			t.date=d['date']

		
			t.transid=d['transid']
			t.investment=d['investment']
			t.portfolio=d['portfolio']
			t.memo=d['memo']
			t.payee=d['payee']
			t.volume = d['amount']
			t.price=d['price']
			t.cost=d['cost']
		
	

			t.save()
		
			self.transactions.add(t)

	def _filetype(self):

		ext=self.file_name.name.split('.')[1].upper()

		return ext

	def save(self, *args, **kwargs):

		if self._filetype()=='CSV':	
			self._load_data_csv()

		elif self._filetype()=='OFX' or self._filetype()=='QFX':
			self._load_data_ofx()


		self._set_dates_from_data()
		super(TradeDataFile, self).save(*args, **kwargs) # Call the "real" save() method.
		self._create_transactions_from_data()
		super(TradeDataFile, self).save(*args, **kwargs) # Call the "real" save() method.

	def __unicode__(self):
		return str(self.file_name)