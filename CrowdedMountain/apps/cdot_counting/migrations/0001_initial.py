# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'Location'
        db.create_table('cdot_counting_location', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('address', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('city', self.gf('django.db.models.fields.CharField')(max_length=60)),
            ('state_province', self.gf('django.db.models.fields.CharField')(max_length=30)),
            ('country', self.gf('django.db.models.fields.CharField')(max_length=50)),
        ))
        db.send_create_signal('cdot_counting', ['Location'])

        # Adding model 'Resort'
        db.create_table('cdot_counting_resort', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('location', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['cdot_counting.Location'])),
        ))
        db.send_create_signal('cdot_counting', ['Resort'])

        # Adding model 'CountStatistic'
        db.create_table('cdot_counting_countstatistic', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('count', self.gf('django.db.models.fields.IntegerField')()),
            ('date', self.gf('django.db.models.fields.DateTimeField')()),
            ('resort', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['cdot_counting.Resort'])),
        ))
        db.send_create_signal('cdot_counting', ['CountStatistic'])


    def backwards(self, orm):
        
        # Deleting model 'Location'
        db.delete_table('cdot_counting_location')

        # Deleting model 'Resort'
        db.delete_table('cdot_counting_resort')

        # Deleting model 'CountStatistic'
        db.delete_table('cdot_counting_countstatistic')


    models = {
        'cdot_counting.countstatistic': {
            'Meta': {'ordering': "['resort', 'date']", 'object_name': 'CountStatistic'},
            'count': ('django.db.models.fields.IntegerField', [], {}),
            'date': ('django.db.models.fields.DateTimeField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'resort': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['cdot_counting.Resort']"})
        },
        'cdot_counting.location': {
            'Meta': {'object_name': 'Location'},
            'address': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'city': ('django.db.models.fields.CharField', [], {'max_length': '60'}),
            'country': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'state_province': ('django.db.models.fields.CharField', [], {'max_length': '30'})
        },
        'cdot_counting.resort': {
            'Meta': {'object_name': 'Resort'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'location': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['cdot_counting.Location']"}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        }
    }

    complete_apps = ['cdot_counting']
