# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'Investment'
        db.create_table('openportfolioapp_investment', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('company', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['openportfolioapp.Company'])),
            ('asset_class', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['openportfolioapp.AssetClass'])),
            ('currency', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['openportfolioapp.Currency'])),
            ('content_type', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['contenttypes.ContentType'], null=True)),
        ))
        db.send_create_signal('openportfolioapp', ['Investment'])

        # Adding model 'TradeAllocation'
        db.create_table('openportfolioapp_tradeallocation', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('buy_trade', self.gf('django.db.models.fields.related.ForeignKey')(related_name='+', to=orm['openportfolioapp.Trade'])),
            ('sell_trade', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['openportfolioapp.Trade'])),
            ('volume', self.gf('django.db.models.fields.DecimalField')(max_digits=20, decimal_places=2)),
        ))
        db.send_create_signal('openportfolioapp', ['TradeAllocation'])

        # Adding model 'Trade'
        db.create_table('openportfolioapp_trade', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('date', self.gf('django.db.models.fields.DateField')()),
            ('volume', self.gf('django.db.models.fields.DecimalField')(max_digits=20, decimal_places=2)),
            ('price', self.gf('django.db.models.fields.DecimalField')(max_digits=20, decimal_places=6)),
            ('cost', self.gf('django.db.models.fields.DecimalField')(max_digits=20, decimal_places=2)),
            ('trade_type', self.gf('django.db.models.fields.CharField')(max_length=3)),
            ('memo', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('payee', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('portfolio', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['openportfolioapp.Portfolio'])),
            ('investment', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['openportfolioapp.Investment'])),
            ('transid', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
        ))
        db.send_create_signal('openportfolioapp', ['Trade'])

        # Adding model 'Portfolio'
        db.create_table('openportfolioapp_portfolio', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('parent', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='child', null=True, to=orm['openportfolioapp.Portfolio'])),
            ('bm', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='benchmark', null=True, to=orm['openportfolioapp.Portfolio'])),
        ))
        db.send_create_signal('openportfolioapp', ['Portfolio'])

        # Adding model 'AssetClass'
        db.create_table('openportfolioapp_assetclass', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('parent', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='child', null=True, to=orm['openportfolioapp.AssetClass'])),
            ('benchmark', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['openportfolioapp.Portfolio'])),
        ))
        db.send_create_signal('openportfolioapp', ['AssetClass'])

        # Adding model 'GICSSector'
        db.create_table('openportfolioapp_gicssector', (
            ('code', self.gf('django.db.models.fields.CharField')(max_length=8, primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('description', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('level', self.gf('django.db.models.fields.CharField')(max_length=13)),
            ('parent', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='child', null=True, to=orm['openportfolioapp.GICSSector'])),
        ))
        db.send_create_signal('openportfolioapp', ['GICSSector'])

        # Adding model 'Company'
        db.create_table('openportfolioapp_company', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('gics_sector', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['openportfolioapp.GICSSector'])),
        ))
        db.send_create_signal('openportfolioapp', ['Company'])

        # Adding model 'Price'
        db.create_table('openportfolioapp_price', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('date', self.gf('django.db.models.fields.DateField')()),
            ('price', self.gf('django.db.models.fields.DecimalField')(default=-1, max_digits=20, decimal_places=4)),
            ('content_type', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['contenttypes.ContentType'], null=True)),
        ))
        db.send_create_signal('openportfolioapp', ['Price'])

        # Adding model 'InvestmentPrice'
        db.create_table('openportfolioapp_investmentprice', (
            ('price_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['openportfolioapp.Price'], unique=True, primary_key=True)),
            ('investment', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['openportfolioapp.Investment'])),
            ('dividend', self.gf('django.db.models.fields.DecimalField')(default=-1, max_digits=20, decimal_places=10)),
        ))
        db.send_create_signal('openportfolioapp', ['InvestmentPrice'])

        # Adding model 'ListedEquityPrice'
        db.create_table('openportfolioapp_listedequityprice', (
            ('investmentprice_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['openportfolioapp.InvestmentPrice'], unique=True, primary_key=True)),
            ('close', self.gf('django.db.models.fields.DecimalField')(default=-1, max_digits=20, decimal_places=4)),
            ('adj_close', self.gf('django.db.models.fields.DecimalField')(default=-1, max_digits=20, decimal_places=4)),
            ('high', self.gf('django.db.models.fields.DecimalField')(default=-1, max_digits=20, decimal_places=4)),
            ('low', self.gf('django.db.models.fields.DecimalField')(default=-1, max_digits=20, decimal_places=4)),
            ('open', self.gf('django.db.models.fields.DecimalField')(default=-1, max_digits=20, decimal_places=4)),
            ('volume', self.gf('django.db.models.fields.DecimalField')(default=-1, max_digits=20, decimal_places=0)),
        ))
        db.send_create_signal('openportfolioapp', ['ListedEquityPrice'])

        # Adding model 'CurrencyPrice'
        db.create_table('openportfolioapp_currencyprice', (
            ('price_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['openportfolioapp.Price'], unique=True, primary_key=True)),
            ('currency', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['openportfolioapp.Currency'])),
        ))
        db.send_create_signal('openportfolioapp', ['CurrencyPrice'])

        # Adding model 'SavingsAccountPrice'
        db.create_table('openportfolioapp_savingsaccountprice', (
            ('investmentprice_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['openportfolioapp.InvestmentPrice'], unique=True, primary_key=True)),
        ))
        db.send_create_signal('openportfolioapp', ['SavingsAccountPrice'])

        # Adding model 'PortfolioPrice'
        db.create_table('openportfolioapp_portfolioprice', (
            ('price_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['openportfolioapp.Price'], unique=True, primary_key=True)),
            ('portfolio', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['openportfolioapp.Portfolio'])),
            ('marketvalue', self.gf('django.db.models.fields.DecimalField')(default=-1, max_digits=20, decimal_places=4)),
            ('numholdings', self.gf('django.db.models.fields.IntegerField')(default=-1)),
        ))
        db.send_create_signal('openportfolioapp', ['PortfolioPrice'])

        # Adding model 'Currency'
        db.create_table('openportfolioapp_currency', (
            ('code', self.gf('django.db.models.fields.CharField')(max_length=6, primary_key=True)),
            ('locale_code', self.gf('django.db.models.fields.CharField')(max_length=6)),
        ))
        db.send_create_signal('openportfolioapp', ['Currency'])

        # Adding model 'ListedEquity'
        db.create_table('openportfolioapp_listedequity', (
            ('investment_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['openportfolioapp.Investment'], unique=True, primary_key=True)),
            ('ticker', self.gf('django.db.models.fields.CharField')(max_length=5)),
            ('exchange_code', self.gf('django.db.models.fields.CharField')(max_length=4, null=True, blank=True)),
        ))
        db.send_create_signal('openportfolioapp', ['ListedEquity'])

        # Adding model 'InterestRate'
        db.create_table('openportfolioapp_interestrate', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('investment', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['openportfolioapp.Investment'])),
            ('date', self.gf('django.db.models.fields.DateField')()),
            ('annualrate', self.gf('django.db.models.fields.DecimalField')(default=-1, max_digits=20, decimal_places=4)),
        ))
        db.send_create_signal('openportfolioapp', ['InterestRate'])

        # Adding model 'SavingsAccount'
        db.create_table('openportfolioapp_savingsaccount', (
            ('investment_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['openportfolioapp.Investment'], unique=True, primary_key=True)),
        ))
        db.send_create_signal('openportfolioapp', ['SavingsAccount'])

        # Adding model 'DataDefinition'
        db.create_table('openportfolioapp_datadefinition', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('investment', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['openportfolioapp.Investment'])),
            ('headers', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('skip_rows', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('date_col', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('memo_col', self.gf('django.db.models.fields.IntegerField')(default=-1)),
            ('payee_col', self.gf('django.db.models.fields.IntegerField')(default=-1)),
            ('debit_col', self.gf('django.db.models.fields.IntegerField')(default=-1)),
            ('credit_col', self.gf('django.db.models.fields.IntegerField')(default=-1)),
            ('balance_col', self.gf('django.db.models.fields.IntegerField')(default=-1)),
            ('price_col', self.gf('django.db.models.fields.IntegerField')(default=-1)),
            ('cost_col', self.gf('django.db.models.fields.IntegerField')(default=-1)),
            ('date_format', self.gf('django.db.models.fields.CharField')(default='%d/%m/%Y', max_length=10)),
        ))
        db.send_create_signal('openportfolioapp', ['DataDefinition'])

        # Adding model 'TradeDataFile'
        db.create_table('openportfolioapp_tradedatafile', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('start_date', self.gf('django.db.models.fields.DateField')()),
            ('end_date', self.gf('django.db.models.fields.DateField')()),
            ('file_name', self.gf('django.db.models.fields.files.FileField')(max_length=100)),
            ('investment', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['openportfolioapp.Investment'], null=True, blank=True)),
            ('portfolio', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['openportfolioapp.Portfolio'], null=True, blank=True)),
            ('bulkfile', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('openportfolioapp', ['TradeDataFile'])

        # Adding M2M table for field transactions on 'TradeDataFile'
        db.create_table('openportfolioapp_tradedatafile_transactions', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('tradedatafile', models.ForeignKey(orm['openportfolioapp.tradedatafile'], null=False)),
            ('trade', models.ForeignKey(orm['openportfolioapp.trade'], null=False))
        ))
        db.create_unique('openportfolioapp_tradedatafile_transactions', ['tradedatafile_id', 'trade_id'])


    def backwards(self, orm):
        
        # Deleting model 'Investment'
        db.delete_table('openportfolioapp_investment')

        # Deleting model 'TradeAllocation'
        db.delete_table('openportfolioapp_tradeallocation')

        # Deleting model 'Trade'
        db.delete_table('openportfolioapp_trade')

        # Deleting model 'Portfolio'
        db.delete_table('openportfolioapp_portfolio')

        # Deleting model 'AssetClass'
        db.delete_table('openportfolioapp_assetclass')

        # Deleting model 'GICSSector'
        db.delete_table('openportfolioapp_gicssector')

        # Deleting model 'Company'
        db.delete_table('openportfolioapp_company')

        # Deleting model 'Price'
        db.delete_table('openportfolioapp_price')

        # Deleting model 'InvestmentPrice'
        db.delete_table('openportfolioapp_investmentprice')

        # Deleting model 'ListedEquityPrice'
        db.delete_table('openportfolioapp_listedequityprice')

        # Deleting model 'CurrencyPrice'
        db.delete_table('openportfolioapp_currencyprice')

        # Deleting model 'SavingsAccountPrice'
        db.delete_table('openportfolioapp_savingsaccountprice')

        # Deleting model 'PortfolioPrice'
        db.delete_table('openportfolioapp_portfolioprice')

        # Deleting model 'Currency'
        db.delete_table('openportfolioapp_currency')

        # Deleting model 'ListedEquity'
        db.delete_table('openportfolioapp_listedequity')

        # Deleting model 'InterestRate'
        db.delete_table('openportfolioapp_interestrate')

        # Deleting model 'SavingsAccount'
        db.delete_table('openportfolioapp_savingsaccount')

        # Deleting model 'DataDefinition'
        db.delete_table('openportfolioapp_datadefinition')

        # Deleting model 'TradeDataFile'
        db.delete_table('openportfolioapp_tradedatafile')

        # Removing M2M table for field transactions on 'TradeDataFile'
        db.delete_table('openportfolioapp_tradedatafile_transactions')


    models = {
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'openportfolioapp.assetclass': {
            'Meta': {'object_name': 'AssetClass'},
            'benchmark': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['openportfolioapp.Portfolio']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'parent': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'child'", 'null': 'True', 'to': "orm['openportfolioapp.AssetClass']"})
        },
        'openportfolioapp.company': {
            'Meta': {'object_name': 'Company'},
            'gics_sector': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['openportfolioapp.GICSSector']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'openportfolioapp.currency': {
            'Meta': {'object_name': 'Currency'},
            'code': ('django.db.models.fields.CharField', [], {'max_length': '6', 'primary_key': 'True'}),
            'locale_code': ('django.db.models.fields.CharField', [], {'max_length': '6'})
        },
        'openportfolioapp.currencyprice': {
            'Meta': {'object_name': 'CurrencyPrice', '_ormbases': ['openportfolioapp.Price']},
            'currency': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['openportfolioapp.Currency']"}),
            'price_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['openportfolioapp.Price']", 'unique': 'True', 'primary_key': 'True'})
        },
        'openportfolioapp.datadefinition': {
            'Meta': {'object_name': 'DataDefinition'},
            'balance_col': ('django.db.models.fields.IntegerField', [], {'default': '-1'}),
            'cost_col': ('django.db.models.fields.IntegerField', [], {'default': '-1'}),
            'credit_col': ('django.db.models.fields.IntegerField', [], {'default': '-1'}),
            'date_col': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'date_format': ('django.db.models.fields.CharField', [], {'default': "'%d/%m/%Y'", 'max_length': '10'}),
            'debit_col': ('django.db.models.fields.IntegerField', [], {'default': '-1'}),
            'headers': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'investment': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['openportfolioapp.Investment']"}),
            'memo_col': ('django.db.models.fields.IntegerField', [], {'default': '-1'}),
            'payee_col': ('django.db.models.fields.IntegerField', [], {'default': '-1'}),
            'price_col': ('django.db.models.fields.IntegerField', [], {'default': '-1'}),
            'skip_rows': ('django.db.models.fields.IntegerField', [], {'default': '0'})
        },
        'openportfolioapp.gicssector': {
            'Meta': {'object_name': 'GICSSector'},
            'code': ('django.db.models.fields.CharField', [], {'max_length': '8', 'primary_key': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'level': ('django.db.models.fields.CharField', [], {'max_length': '13'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'parent': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'child'", 'null': 'True', 'to': "orm['openportfolioapp.GICSSector']"})
        },
        'openportfolioapp.interestrate': {
            'Meta': {'object_name': 'InterestRate'},
            'annualrate': ('django.db.models.fields.DecimalField', [], {'default': '-1', 'max_digits': '20', 'decimal_places': '4'}),
            'date': ('django.db.models.fields.DateField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'investment': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['openportfolioapp.Investment']"})
        },
        'openportfolioapp.investment': {
            'Meta': {'object_name': 'Investment'},
            'asset_class': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['openportfolioapp.AssetClass']"}),
            'company': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['openportfolioapp.Company']"}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']", 'null': 'True'}),
            'currency': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['openportfolioapp.Currency']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'openportfolioapp.investmentprice': {
            'Meta': {'object_name': 'InvestmentPrice', '_ormbases': ['openportfolioapp.Price']},
            'dividend': ('django.db.models.fields.DecimalField', [], {'default': '-1', 'max_digits': '20', 'decimal_places': '10'}),
            'investment': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['openportfolioapp.Investment']"}),
            'price_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['openportfolioapp.Price']", 'unique': 'True', 'primary_key': 'True'})
        },
        'openportfolioapp.listedequity': {
            'Meta': {'object_name': 'ListedEquity', '_ormbases': ['openportfolioapp.Investment']},
            'exchange_code': ('django.db.models.fields.CharField', [], {'max_length': '4', 'null': 'True', 'blank': 'True'}),
            'investment_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['openportfolioapp.Investment']", 'unique': 'True', 'primary_key': 'True'}),
            'ticker': ('django.db.models.fields.CharField', [], {'max_length': '5'})
        },
        'openportfolioapp.listedequityprice': {
            'Meta': {'object_name': 'ListedEquityPrice', '_ormbases': ['openportfolioapp.InvestmentPrice']},
            'adj_close': ('django.db.models.fields.DecimalField', [], {'default': '-1', 'max_digits': '20', 'decimal_places': '4'}),
            'close': ('django.db.models.fields.DecimalField', [], {'default': '-1', 'max_digits': '20', 'decimal_places': '4'}),
            'high': ('django.db.models.fields.DecimalField', [], {'default': '-1', 'max_digits': '20', 'decimal_places': '4'}),
            'investmentprice_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['openportfolioapp.InvestmentPrice']", 'unique': 'True', 'primary_key': 'True'}),
            'low': ('django.db.models.fields.DecimalField', [], {'default': '-1', 'max_digits': '20', 'decimal_places': '4'}),
            'open': ('django.db.models.fields.DecimalField', [], {'default': '-1', 'max_digits': '20', 'decimal_places': '4'}),
            'volume': ('django.db.models.fields.DecimalField', [], {'default': '-1', 'max_digits': '20', 'decimal_places': '0'})
        },
        'openportfolioapp.portfolio': {
            'Meta': {'object_name': 'Portfolio'},
            'bm': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'benchmark'", 'null': 'True', 'to': "orm['openportfolioapp.Portfolio']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'parent': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'child'", 'null': 'True', 'to': "orm['openportfolioapp.Portfolio']"})
        },
        'openportfolioapp.portfolioprice': {
            'Meta': {'object_name': 'PortfolioPrice', '_ormbases': ['openportfolioapp.Price']},
            'marketvalue': ('django.db.models.fields.DecimalField', [], {'default': '-1', 'max_digits': '20', 'decimal_places': '4'}),
            'numholdings': ('django.db.models.fields.IntegerField', [], {'default': '-1'}),
            'portfolio': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['openportfolioapp.Portfolio']"}),
            'price_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['openportfolioapp.Price']", 'unique': 'True', 'primary_key': 'True'})
        },
        'openportfolioapp.price': {
            'Meta': {'object_name': 'Price'},
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']", 'null': 'True'}),
            'date': ('django.db.models.fields.DateField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'price': ('django.db.models.fields.DecimalField', [], {'default': '-1', 'max_digits': '20', 'decimal_places': '4'})
        },
        'openportfolioapp.savingsaccount': {
            'Meta': {'object_name': 'SavingsAccount', '_ormbases': ['openportfolioapp.Investment']},
            'investment_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['openportfolioapp.Investment']", 'unique': 'True', 'primary_key': 'True'})
        },
        'openportfolioapp.savingsaccountprice': {
            'Meta': {'object_name': 'SavingsAccountPrice', '_ormbases': ['openportfolioapp.InvestmentPrice']},
            'investmentprice_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['openportfolioapp.InvestmentPrice']", 'unique': 'True', 'primary_key': 'True'})
        },
        'openportfolioapp.trade': {
            'Meta': {'object_name': 'Trade'},
            'cost': ('django.db.models.fields.DecimalField', [], {'max_digits': '20', 'decimal_places': '2'}),
            'date': ('django.db.models.fields.DateField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'investment': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['openportfolioapp.Investment']"}),
            'memo': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'payee': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'portfolio': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['openportfolioapp.Portfolio']"}),
            'price': ('django.db.models.fields.DecimalField', [], {'max_digits': '20', 'decimal_places': '6'}),
            'trade_type': ('django.db.models.fields.CharField', [], {'max_length': '3'}),
            'transid': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'volume': ('django.db.models.fields.DecimalField', [], {'max_digits': '20', 'decimal_places': '2'})
        },
        'openportfolioapp.tradeallocation': {
            'Meta': {'object_name': 'TradeAllocation'},
            'buy_trade': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'+'", 'to': "orm['openportfolioapp.Trade']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'sell_trade': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['openportfolioapp.Trade']"}),
            'volume': ('django.db.models.fields.DecimalField', [], {'max_digits': '20', 'decimal_places': '2'})
        },
        'openportfolioapp.tradedatafile': {
            'Meta': {'object_name': 'TradeDataFile'},
            'bulkfile': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'end_date': ('django.db.models.fields.DateField', [], {}),
            'file_name': ('django.db.models.fields.files.FileField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'investment': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['openportfolioapp.Investment']", 'null': 'True', 'blank': 'True'}),
            'portfolio': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['openportfolioapp.Portfolio']", 'null': 'True', 'blank': 'True'}),
            'start_date': ('django.db.models.fields.DateField', [], {}),
            'transactions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['openportfolioapp.Trade']", 'symmetrical': 'False'})
        }
    }

    complete_apps = ['openportfolioapp']
