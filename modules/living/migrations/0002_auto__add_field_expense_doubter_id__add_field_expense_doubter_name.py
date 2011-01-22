# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding field 'Expense.doubter_id'
        db.add_column('living_expense', 'doubter_id', self.gf('django.db.models.fields.IntegerField')(default=0), keep_default=False)

        # Adding field 'Expense.doubter_name'
        db.add_column('living_expense', 'doubter_name', self.gf('django.db.models.fields.CharField')(default='', max_length=30), keep_default=False)


    def backwards(self, orm):
        
        # Deleting field 'Expense.doubter_id'
        db.delete_column('living_expense', 'doubter_id')

        # Deleting field 'Expense.doubter_name'
        db.delete_column('living_expense', 'doubter_name')


    models = {
        'living.balance': {
            'Meta': {'object_name': 'Balance'},
            'balance': ('django.db.models.fields.FloatField', [], {}),
            'balance_id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'user_id': ('django.db.models.fields.IntegerField', [], {'db_index': 'True'}),
            'user_name': ('django.db.models.fields.CharField', [], {'max_length': '30'})
        },
        'living.comment': {
            'Meta': {'object_name': 'Comment'},
            'comment_id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'created_on': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'is_valid': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'message': ('django.db.models.fields.IntegerField', [], {'max_length': '65536'}),
            'modified_on': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'target_id': ('django.db.models.fields.IntegerField', [], {'db_index': 'True'}),
            'target_name': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            'user_id': ('django.db.models.fields.IntegerField', [], {'db_index': 'True'}),
            'user_name': ('django.db.models.fields.CharField', [], {'max_length': '30'})
        },
        'living.expense': {
            'Meta': {'object_name': 'Expense'},
            'amount': ('django.db.models.fields.FloatField', [], {}),
            'consumer_ids': ('django.db.models.fields.CommaSeparatedIntegerField', [], {'max_length': '1024'}),
            'consumer_names': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '65536'}),
            'created_on': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'creater_id': ('django.db.models.fields.IntegerField', [], {'db_index': 'True'}),
            'creater_name': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'doubter_id': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'doubter_name': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '30'}),
            'expense_id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'in_doubt': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_valid': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'message': ('django.db.models.fields.TextField', [], {'max_length': '65536'}),
            'modified_on': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'payer_ids': ('django.db.models.fields.CommaSeparatedIntegerField', [], {'max_length': '1024'}),
            'payer_names': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '65536'}),
            'spent_on': ('django.db.models.fields.DateField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'subject': ('django.db.models.fields.CharField', [], {'max_length': '80'}),
            'tags': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'living.myindex': {
            'Meta': {'object_name': 'MyIndex'},
            'comment_ids': ('django.db.models.fields.CommaSeparatedIntegerField', [], {'default': "''", 'max_length': '65536'}),
            'expense_ids': ('django.db.models.fields.CommaSeparatedIntegerField', [], {'default': "''", 'max_length': '65536'}),
            'myindex_id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'recurring_ids': ('django.db.models.fields.CommaSeparatedIntegerField', [], {'default': "''", 'max_length': '65536'}),
            'user_id': ('django.db.models.fields.IntegerField', [], {'db_index': 'True'}),
            'user_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'db_index': 'True'})
        },
        'living.recurring': {
            'Meta': {'object_name': 'Recurring'},
            'amount': ('django.db.models.fields.FloatField', [], {}),
            'consumer_ids': ('django.db.models.fields.CommaSeparatedIntegerField', [], {'max_length': '1024'}),
            'consumer_names': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '65536'}),
            'created_on': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'creater_id': ('django.db.models.fields.IntegerField', [], {'db_index': 'True'}),
            'creater_name': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'in_doubt': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_valid': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'last_recurred': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'message': ('django.db.models.fields.TextField', [], {'max_length': '65536'}),
            'modified_on': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'period': ('django.db.models.fields.IntegerField', [], {}),
            'recurring_id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'started_on': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'subject': ('django.db.models.fields.CharField', [], {'max_length': '80'}),
            'tags': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'living.tag': {
            'Meta': {'object_name': 'Tag'},
            'expense_ids': ('django.db.models.fields.CommaSeparatedIntegerField', [], {'default': "''", 'max_length': '65536'}),
            'tag_id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'tag_name': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'total': ('django.db.models.fields.FloatField', [], {})
        }
    }

    complete_apps = ['living']
