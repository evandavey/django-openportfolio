from django.contrib import admin
from django.contrib.contenttypes.models import ContentType
from django.http import HttpResponseRedirect

from openportfolioapp.models import *
from openportfolioapp.models.investments import *

class AssetClassAdmin(admin.ModelAdmin):
	""" Object to control the behaviour of the linked object in the Admin interface
	"""
	list_display = ['full_name','name']
	list_filter = []
	ordering = ['name']
	search_fields = ['name']


class GICSSectorAdmin(admin.ModelAdmin):
	""" Object to control the behaviour of the linked object in the Admin interface
	"""
	list_display = ['full_name','name', 'level']
	list_filter = ['level']
	ordering = ['level']
	search_fields = ['name']

class TradeAdmin(admin.ModelAdmin):
	""" Object to control the behaviour of the linked object in the Admin interface
	"""
	list_display = ['date','trade_type','portfolio','investment','volume','price','cost','memo']
	list_filter = ['investment','portfolio','date']
	ordering = []
	search_fields = []
	readonly_fields=[]

class InvestmentAdmin(admin.ModelAdmin):
	""" Object to control the behaviour of the linked object in the Admin interface
	"""
	list_display = ['name','latest_price','latest_price_date','latest_dividend','latest_dividend_date']
	list_filter = []
	ordering = ['name']
	search_fields = ['name']
	
class TradeAllocationAdmin(admin.ModelAdmin):
	
	
	list_display=['date','portfolio','investment','sell_price','buy_price','volume','cost','profit']

class ListedEquityPriceAdmin(admin.ModelAdmin):


	list_display=['date','investment','price','dividend']
	list_filter = ['investment']

class SavingsAccountPriceAdmin(admin.ModelAdmin):


		list_display=['date','investment','price','dividend']
		list_filter = ['investment']

class CurrencyPriceAdmin(admin.ModelAdmin):


		list_display=['date','currency','price']
		list_filter = ['currency']


class PortfolioAdmin(admin.ModelAdmin):
	
	list_display=['full_name']


class InterestRateAdmin(admin.ModelAdmin):


	list_display=['date','investment','annualrate']
	list_filter = ['investment']
	
class TradeDataFileAdmin(admin.ModelAdmin):
    
    list_display=['file_name','start_date','end_date','portfolio','investment','bulkfile']
    
class ListedEquityAdmin(admin.ModelAdmin):
    
    list_display=['name','full_ticker']
    
class SavingsAccountAdmin(admin.ModelAdmin):
    
    list_display=['name']
    
class CompanyAdmin(admin.ModelAdmin):
    
    list_display=['name','gics_sector']
    
class CurrencyAdmin(admin.ModelAdmin):
    
    list_display=['code','locale_code']

admin.site.register(AssetClass,AssetClassAdmin)	
admin.site.register(GICSSector,GICSSectorAdmin)	
admin.site.register(Company,CompanyAdmin)	
admin.site.register(Portfolio,PortfolioAdmin)
admin.site.register(Investment,InvestmentAdmin)
admin.site.register(ListedEquity,ListedEquityAdmin)
admin.site.register(SavingsAccount,SavingsAccountAdmin)
admin.site.register(Currency,CurrencyAdmin)
admin.site.register(Trade,TradeAdmin)
admin.site.register(ListedEquityPrice,ListedEquityPriceAdmin)
admin.site.register(CurrencyPrice,CurrencyPriceAdmin)
admin.site.register(TradeAllocation,TradeAllocationAdmin)
admin.site.register(TradeDataFile,TradeDataFileAdmin)
admin.site.register(DataDefinition)
admin.site.register(InterestRate,InterestRateAdmin)
admin.site.register(SavingsAccountPrice,SavingsAccountPriceAdmin)








	
