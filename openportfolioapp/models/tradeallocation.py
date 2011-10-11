from django.db import models
	
class TradeAllocation(models.Model):
	""" Object to allocate sell trades against buy trades
	"""
	
	class Meta:
		verbose_name_plural = "Trade Allocations" #cleans up name in admin
		app_label = "openportfolioapp"
			
	buy_trade=models.ForeignKey("Trade",related_name='+')
	sell_trade=models.ForeignKey("Trade")
	volume=models.DecimalField(decimal_places=2,max_digits=20)
	#cost_allocation=models.DecimalField(decimal_places=2,max_digits=20)
	

	def _profit(self):
		
		return ((self.sell_price-self.buy_price)*self.volume)-self.cost
		
	profit=property(_profit)
		
	
	def _investment(self):
		return self.sell_trade.investment
	investment=property(_investment)
		
	def _portfolio(self):
		return self.sell_trade.portfolio
	portfolio=property(_portfolio)
	
	def _date(self):
		return self.sell_trade.date
	date=property(_date)
	
	def _sell_price(self):
		return self.sell_trade.price
	sell_price=property(_sell_price)
	
	def _buy_price(self):
		return self.buy_trade.price
	buy_price=property(_buy_price)
	
	def _cost(self):
		cost=0
		cost+=(self.buy_trade.cost/self.buy_trade.volume)*self.volume
		cost+=self.sell_trade.cost
	
		return cost
	
	cost=property(_cost)