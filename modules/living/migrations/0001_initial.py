# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'Expense'
        db.create_table('living_expense', (
            ('expense_id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('creater_id', self.gf('django.db.models.fields.IntegerField')(db_index=True)),
            ('creater_name', self.gf('django.db.models.fields.CharField')(max_length=30)),
            ('subject', self.gf('django.db.models.fields.CharField')(max_length=80)),
            ('message', self.gf('django.db.models.fields.TextField')(max_length=65536)),
            ('amount', self.gf('django.db.models.fields.FloatField')()),
            ('payer_ids', self.gf('django.db.models.fields.CommaSeparatedIntegerField')(max_length=1024)),
            ('payer_names', self.gf('django.db.models.fields.CharField')(default='', max_length=65536)),
            ('consumer_ids', self.gf('django.db.models.fields.CommaSeparatedIntegerField')(max_length=1024)),
            ('consumer_names', self.gf('django.db.models.fields.CharField')(default='', max_length=65536)),
            ('tags', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('spent_on', self.gf('django.db.models.fields.DateField')(auto_now_add=True, blank=True)),
            ('created_on', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('modified_on', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('in_doubt', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('is_valid', self.gf('django.db.models.fields.BooleanField')(default=True)),
        ))
        db.send_create_signal('living', ['Expense'])

        # Adding model 'Recurring'
        db.create_table('living_recurring', (
            ('recurring_id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('creater_id', self.gf('django.db.models.fields.IntegerField')(db_index=True)),
            ('creater_name', self.gf('django.db.models.fields.CharField')(max_length=30)),
            ('subject', self.gf('django.db.models.fields.CharField')(max_length=80)),
            ('message', self.gf('django.db.models.fields.TextField')(max_length=65536)),
            ('amount', self.gf('django.db.models.fields.FloatField')()),
            ('consumer_ids', self.gf('django.db.models.fields.CommaSeparatedIntegerField')(max_length=1024)),
            ('consumer_names', self.gf('django.db.models.fields.CharField')(default='', max_length=65536)),
            ('tags', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('started_on', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('created_on', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('modified_on', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('last_recurred', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('period', self.gf('django.db.models.fields.IntegerField')()),
            ('in_doubt', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('is_valid', self.gf('django.db.models.fields.BooleanField')(default=True)),
        ))
        db.send_create_signal('living', ['Recurring'])

        # Adding model 'Comment'
        db.create_table('living_comment', (
            ('comment_id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('target_id', self.gf('django.db.models.fields.IntegerField')(db_index=True)),
            ('target_name', self.gf('django.db.models.fields.CharField')(max_length=1)),
            ('user_id', self.gf('django.db.models.fields.IntegerField')(db_index=True)),
            ('user_name', self.gf('django.db.models.fields.CharField')(max_length=30)),
            ('message', self.gf('django.db.models.fields.IntegerField')(max_length=65536)),
            ('created_on', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('modified_on', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('is_valid', self.gf('django.db.models.fields.BooleanField')(default=True)),
        ))
        db.send_create_signal('living', ['Comment'])

        # Adding model 'MyIndex'
        db.create_table('living_myindex', (
            ('myindex_id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user_id', self.gf('django.db.models.fields.IntegerField')(db_index=True)),
            ('user_name', self.gf('django.db.models.fields.CharField')(max_length=30, db_index=True)),
            ('expense_ids', self.gf('django.db.models.fields.CommaSeparatedIntegerField')(default='', max_length=65536)),
            ('recurring_ids', self.gf('django.db.models.fields.CommaSeparatedIntegerField')(default='', max_length=65536)),
            ('comment_ids', self.gf('django.db.models.fields.CommaSeparatedIntegerField')(default='', max_length=65536)),
        ))
        db.send_create_signal('living', ['MyIndex'])

        # Adding model 'Tag'
        db.create_table('living_tag', (
            ('tag_id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('tag_name', self.gf('django.db.models.fields.CharField')(max_length=30)),
            ('expense_ids', self.gf('django.db.models.fields.CommaSeparatedIntegerField')(default='', max_length=65536)),
            ('total', self.gf('django.db.models.fields.FloatField')()),
        ))
        db.send_create_signal('living', ['Tag'])

        # Adding model 'Balance'
        db.create_table('living_balance', (
            ('balance_id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user_id', self.gf('django.db.models.fields.IntegerField')(db_index=True)),
            ('user_name', self.gf('django.db.models.fields.CharField')(max_length=30)),
            ('balance', self.gf('django.db.models.fields.FloatField')()),
        ))
        db.send_create_signal('living', ['Balance'])


    def backwards(self, orm):
        
        # Deleting model 'Expense'
        db.delete_table('living_expense')

        # Deleting model 'Recurring'
        db.delete_table('living_recurring')

        # Deleting model 'Comment'
        db.delete_table('living_comment')

        # Deleting model 'MyIndex'
        db.delete_table('living_myindex')

        # Deleting model 'Tag'
        db.delete_table('living_tag')

        # Deleting model 'Balance'
        db.delete_table('living_balance')


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
