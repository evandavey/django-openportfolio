# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Changing field 'TradeDataFile.portfolio'
        db.alter_column('financemanager_tradedatafile', 'portfolio_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['financemanager.Portfolio'], null=True))


    def backwards(self, orm):
        
        # Changing field 'TradeDataFile.portfolio'
        db.alter_column('financemanager_tradedatafile', 'portfolio_id', self.gf('django.db.models.fields.related.ForeignKey')(default=None, to=orm['financemanager.Portfolio']))


    models = {
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'financemanager.assetclass': {
            'Meta': {'object_name': 'AssetClass'},
            'benchmark': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['financemanager.Portfolio']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'parent': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'child'", 'null': 'True', 'to': "orm['financemanager.AssetClass']"})
        },
        'financemanager.company': {
            'Meta': {'object_name': 'Company'},
            'gics_sector': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['financemanager.GICSSector']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'financemanager.currency': {
            'Meta': {'object_name': 'Currency'},
            'code': ('django.db.models.fields.CharField', [], {'max_length': '6', 'primary_key': 'True'}),
            'locale_code': ('django.db.models.fields.CharField', [], {'max_length': '6'})
        },
        'financemanager.currencyprice': {
            'Meta': {'object_name': 'CurrencyPrice', '_ormbases': ['financemanager.Price']},
            'currency': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['financemanager.Currency']"}),
            'price_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['financemanager.Price']", 'unique': 'True', 'primary_key': 'True'})
        },
        'financemanager.datadefinition': {
            'Meta': {'object_name': 'DataDefinition'},
            'balance_col': ('django.db.models.fields.IntegerField', [], {'default': '-1'}),
            'cost_col': ('django.db.models.fields.IntegerField', [], {'default': '-1'}),
            'credit_col': ('django.db.models.fields.IntegerField', [], {'default': '-1'}),
            'date_col': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'date_format': ('django.db.models.fields.CharField', [], {'default': "'%d/%m/%Y'", 'max_length': '10'}),
            'debit_col': ('django.db.models.fields.IntegerField', [], {'default': '-1'}),
            'headers': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'investment': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['financemanager.Investment']"}),
            'memo_col': ('django.db.models.fields.IntegerField', [], {'default': '-1'}),
            'payee_col': ('django.db.models.fields.IntegerField', [], {'default': '-1'}),
            'price_col': ('django.db.models.fields.IntegerField', [], {'default': '-1'}),
            'skip_rows': ('django.db.models.fields.IntegerField', [], {'default': '0'})
        },
        'financemanager.gicssector': {
            'Meta': {'object_name': 'GICSSector'},
            'code': ('django.db.models.fields.CharField', [], {'max_length': '8', 'primary_key': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'level': ('django.db.models.fields.CharField', [], {'max_length': '13'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'parent': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'child'", 'null': 'True', 'to': "orm['financemanager.GICSSector']"})
        },
        'financemanager.investment': {
            'Meta': {'object_name': 'Investment'},
            'asset_class': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['financemanager.AssetClass']"}),
            'company': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['financemanager.Company']"}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']", 'null': 'True'}),
            'currency': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['financemanager.Currency']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'financemanager.listedequity': {
            'Meta': {'object_name': 'ListedEquity', '_ormbases': ['financemanager.Investment']},
            'exchange_code': ('django.db.models.fields.CharField', [], {'max_length': '4'}),
            'investment_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['financemanager.Investment']", 'unique': 'True', 'primary_key': 'True'}),
            'ticker': ('django.db.models.fields.CharField', [], {'max_length': '4'})
        },
        'financemanager.listedequityprice': {
            'Meta': {'object_name': 'ListedEquityPrice', '_ormbases': ['financemanager.Price']},
            'adj_close': ('django.db.models.fields.DecimalField', [], {'default': '-1', 'max_digits': '20', 'decimal_places': '4'}),
            'close': ('django.db.models.fields.DecimalField', [], {'default': '-1', 'max_digits': '20', 'decimal_places': '4'}),
            'dividend': ('django.db.models.fields.DecimalField', [], {'default': '-1', 'max_digits': '20', 'decimal_places': '4'}),
            'high': ('django.db.models.fields.DecimalField', [], {'default': '-1', 'max_digits': '20', 'decimal_places': '4'}),
            'investment': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['financemanager.Investment']"}),
            'low': ('django.db.models.fields.DecimalField', [], {'default': '-1', 'max_digits': '20', 'decimal_places': '4'}),
            'open': ('django.db.models.fields.DecimalField', [], {'default': '-1', 'max_digits': '20', 'decimal_places': '4'}),
            'price_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['financemanager.Price']", 'unique': 'True', 'primary_key': 'True'}),
            'volume': ('django.db.models.fields.DecimalField', [], {'default': '-1', 'max_digits': '20', 'decimal_places': '0'})
        },
        'financemanager.portfolio': {
            'Meta': {'object_name': 'Portfolio'},
            'bm': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'benchmark'", 'null': 'True', 'to': "orm['financemanager.Portfolio']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'parent': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'child'", 'null': 'True', 'to': "orm['financemanager.Portfolio']"})
        },
        'financemanager.price': {
            'Meta': {'object_name': 'Price'},
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']", 'null': 'True'}),
            'date': ('django.db.models.fields.DateField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'price': ('django.db.models.fields.DecimalField', [], {'default': '-1', 'max_digits': '20', 'decimal_places': '4'})
        },
        'financemanager.savingsaccount': {
            'Meta': {'object_name': 'SavingsAccount', '_ormbases': ['financemanager.Investment']},
            'investment_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['financemanager.Investment']", 'unique': 'True', 'primary_key': 'True'})
        },
        'financemanager.trade': {
            'Meta': {'object_name': 'Trade'},
            'cost': ('django.db.models.fields.DecimalField', [], {'max_digits': '20', 'decimal_places': '2'}),
            'date': ('django.db.models.fields.DateField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'investment': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['financemanager.Investment']"}),
            'memo': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'payee': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'portfolio': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['financemanager.Portfolio']"}),
            'price': ('django.db.models.fields.DecimalField', [], {'max_digits': '20', 'decimal_places': '6'}),
            'trade_type': ('django.db.models.fields.CharField', [], {'max_length': '3'}),
            'transid': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True', 'blank': 'True'}),
            'volume': ('django.db.models.fields.DecimalField', [], {'max_digits': '20', 'decimal_places': '2'})
        },
        'financemanager.tradeallocation': {
            'Meta': {'object_name': 'TradeAllocation'},
            'buy_trade': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'+'", 'to': "orm['financemanager.Trade']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'sell_trade': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['financemanager.Trade']"}),
            'volume': ('django.db.models.fields.DecimalField', [], {'max_digits': '20', 'decimal_places': '2'})
        },
        'financemanager.tradedatafile': {
            'Meta': {'object_name': 'TradeDataFile'},
            'bulkfile': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'end_date': ('django.db.models.fields.DateField', [], {}),
            'file_name': ('django.db.models.fields.files.FileField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'investment': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['financemanager.Investment']", 'null': 'True', 'blank': 'True'}),
            'portfolio': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['financemanager.Portfolio']", 'null': 'True', 'blank': 'True'}),
            'start_date': ('django.db.models.fields.DateField', [], {}),
            'transactions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['financemanager.Trade']", 'symmetrical': 'False'})
        }
    }

    complete_apps = ['financemanager']
