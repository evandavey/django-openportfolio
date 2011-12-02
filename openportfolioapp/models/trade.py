from django.db import models
from openportfolioapp.models.investment import Investment
from openportfolioapp.models.tradeallocation import TradeAllocation
class Trade(models.Model):
	""" An object to represent an investment AssetClass
		Each Investment will belong to a single AssetClass
	"""

	class Meta:
		verbose_name_plural = "Trades" #cleans up name in admin
		app_label = "openportfolioapp"

	TRADE_TYPES=(
		('BUY','Buy'),
		('SEL','Sell'),
		('DIV','Dividend'),
		('XFR','Transfer'),
		('OUT','Outflow'),
		('INF','Inflow'),
	)

	date = models.DateField()
	volume = models.DecimalField(decimal_places=2,max_digits=20)
	price = models.DecimalField(decimal_places=6,max_digits=20)
	cost =  models.DecimalField(decimal_places=2,max_digits=20)
	trade_type = models.CharField(max_length=3, choices=TRADE_TYPES,blank=False)
	memo = models.CharField(max_length=255,null=True,blank=True)
	payee = models.CharField(max_length=255,null=True,blank=True)
	portfolio = models.ForeignKey("Portfolio")
	investment = models.ForeignKey("Investment",editable=True)
	transid = models.CharField(max_length=255, null=True,blank=True)
	
	
	def __unicode__(self):
		return str(self.date) + ":" + self.investment.name + ":" + str(self.volume) + ":" + str(self.price)
		
	def _set_trade_type(self):

		if self.volume < 0.0:
			self.trade_type='SEL'
		elif 'INTEREST' in self.memo.upper() or 'DIVIDEND' in self.memo.upper():
			self.trade_type='DIV'
		else:
		   
		    self.trade_type='BUY'
	
	def save(self, *args, **kwargs):
	    
	    
	    if self.trade_type is None:
	        self._set_trade_type()
	        
	    super(Trade, self).save(*args, **kwargs) # Call the "real" save() method.	
	    #workaround code to trigger subclass process trade function
	    i=self.investment
	    content_type = i.content_type
	    model = content_type.model_class()
	    i=model.objects.get(pk=i.id)
	    i.process_trade(self)
	    
		
	def profit(self):
		
		if self.trade_type=='SEL':
			alloc=TradeAllocation.objects.filter(sell_trade=self)
			
			if len(alloc)==0:
				return None
				
			else:
				profit=0
				for a in alloc:
					profit+=a.profit
					
				return profit
			
		
		return None
		
		