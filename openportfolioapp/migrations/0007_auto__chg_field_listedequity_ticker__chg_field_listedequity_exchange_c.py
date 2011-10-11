# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Changing field 'ListedEquity.ticker'
        db.alter_column('openportfolioapp_listedequity', 'ticker', self.gf('django.db.models.fields.CharField')(max_length=5))

        # Changing field 'ListedEquity.exchange_code'
        db.alter_column('openportfolioapp_listedequity', 'exchange_code', self.gf('django.db.models.fields.CharField')(max_length=4, null=True))


    def backwards(self, orm):
        
        # Changing field 'ListedEquity.ticker'
        db.alter_column('openportfolioapp_listedequity', 'ticker', self.gf('django.db.models.fields.CharField')(max_length=4))

        # Changing field 'ListedEquity.exchange_code'
        db.alter_column('openportfolioapp_listedequity', 'exchange_code', self.gf('django.db.models.fields.CharField')(default=None, max_length=4))


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
        'openportfolioapp.listedequity': {
            'Meta': {'object_name': 'ListedEquity', '_ormbases': ['openportfolioapp.Investment']},
            'exchange_code': ('django.db.models.fields.CharField', [], {'max_length': '4', 'null': 'True', 'blank': 'True'}),
            'investment_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['openportfolioapp.Investment']", 'unique': 'True', 'primary_key': 'True'}),
            'ticker': ('django.db.models.fields.CharField', [], {'max_length': '5'})
        },
        'openportfolioapp.listedequityprice': {
            'Meta': {'object_name': 'ListedEquityPrice', '_ormbases': ['openportfolioapp.Price']},
            'adj_close': ('django.db.models.fields.DecimalField', [], {'default': '-1', 'max_digits': '20', 'decimal_places': '4'}),
            'close': ('django.db.models.fields.DecimalField', [], {'default': '-1', 'max_digits': '20', 'decimal_places': '4'}),
            'dividend': ('django.db.models.fields.DecimalField', [], {'default': '-1', 'max_digits': '20', 'decimal_places': '10'}),
            'high': ('django.db.models.fields.DecimalField', [], {'default': '-1', 'max_digits': '20', 'decimal_places': '4'}),
            'investment': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['openportfolioapp.Investment']"}),
            'low': ('django.db.models.fields.DecimalField', [], {'default': '-1', 'max_digits': '20', 'decimal_places': '4'}),
            'open': ('django.db.models.fields.DecimalField', [], {'default': '-1', 'max_digits': '20', 'decimal_places': '4'}),
            'price_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['openportfolioapp.Price']", 'unique': 'True', 'primary_key': 'True'}),
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
            'Meta': {'object_name': 'SavingsAccountPrice', '_ormbases': ['openportfolioapp.Price']},
            'dividend': ('django.db.models.fields.DecimalField', [], {'default': '-1', 'max_digits': '20', 'decimal_places': '10'}),
            'investment': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['openportfolioapp.Investment']"}),
            'price_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['openportfolioapp.Price']", 'unique': 'True', 'primary_key': 'True'})
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
            'transid': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True', 'blank': 'True'}),
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
