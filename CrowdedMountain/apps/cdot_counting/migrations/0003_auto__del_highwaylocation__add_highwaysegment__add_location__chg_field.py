# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting model 'HighwayLocation'
        db.delete_table(u'cdot_counting_highwaylocation')

        # Adding model 'HighwaySegment'
        db.create_table(u'cdot_counting_highwaysegment', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('start_mile_marker', self.gf('django.db.models.fields.DecimalField')(max_digits=8, decimal_places=2)),
            ('end_mile_marker', self.gf('django.db.models.fields.DecimalField')(max_digits=8, decimal_places=2)),
            ('direction', self.gf('django.db.models.fields.CharField')(max_length=10)),
            ('datetime_calculated', self.gf('django.db.models.fields.DateTimeField')()),
            ('current_travel_time', self.gf('django.db.models.fields.IntegerField')()),
            ('expected_travel_time', self.gf('django.db.models.fields.IntegerField')()),
            ('avg_volume', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('avg_occupancy', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
        ))
        db.send_create_signal(u'cdot_counting', ['HighwaySegment'])

        # Adding model 'Location'
        db.create_table(u'cdot_counting_location', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('address', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('city', self.gf('django.db.models.fields.CharField')(max_length=60)),
            ('state_province', self.gf('django.db.models.fields.CharField')(max_length=30)),
            ('country', self.gf('django.db.models.fields.CharField')(max_length=50)),
        ))
        db.send_create_signal(u'cdot_counting', ['Location'])


        # Changing field 'Resort.location'
        db.alter_column(u'cdot_counting_resort', 'location_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['cdot_counting.Location']))

    def backwards(self, orm):
        # Adding model 'HighwayLocation'
        db.create_table(u'cdot_counting_highwaylocation', (
            ('milemarker_low', self.gf('django.db.models.fields.DecimalField')(max_digits=8, decimal_places=2)),
            ('city', self.gf('django.db.models.fields.CharField')(max_length=60)),
            ('state_province', self.gf('django.db.models.fields.CharField')(max_length=30)),
            ('address', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('milemarker_high', self.gf('django.db.models.fields.DecimalField')(max_digits=8, decimal_places=2)),
            ('country', self.gf('django.db.models.fields.CharField')(max_length=50)),
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
        ))
        db.send_create_signal(u'cdot_counting', ['HighwayLocation'])

        # Deleting model 'HighwaySegment'
        db.delete_table(u'cdot_counting_highwaysegment')

        # Deleting model 'Location'
        db.delete_table(u'cdot_counting_location')


        # Changing field 'Resort.location'
        db.alter_column(u'cdot_counting_resort', 'location_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['cdot_counting.HighwayLocation']))

    models = {
        u'cdot_counting.countstatistic': {
            'Meta': {'ordering': "['resort', 'date']", 'object_name': 'CountStatistic'},
            'count': ('django.db.models.fields.IntegerField', [], {}),
            'date': ('django.db.models.fields.DateTimeField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'resort': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['cdot_counting.Resort']"})
        },
        u'cdot_counting.highwaysegment': {
            'Meta': {'object_name': 'HighwaySegment'},
            'avg_occupancy': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'avg_volume': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'current_travel_time': ('django.db.models.fields.IntegerField', [], {}),
            'datetime_calculated': ('django.db.models.fields.DateTimeField', [], {}),
            'direction': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'end_mile_marker': ('django.db.models.fields.DecimalField', [], {'max_digits': '8', 'decimal_places': '2'}),
            'expected_travel_time': ('django.db.models.fields.IntegerField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'start_mile_marker': ('django.db.models.fields.DecimalField', [], {'max_digits': '8', 'decimal_places': '2'})
        },
        u'cdot_counting.location': {
            'Meta': {'object_name': 'Location'},
            'address': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'city': ('django.db.models.fields.CharField', [], {'max_length': '60'}),
            'country': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'state_province': ('django.db.models.fields.CharField', [], {'max_length': '30'})
        },
        u'cdot_counting.resort': {
            'Meta': {'ordering': "['name']", 'object_name': 'Resort'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'location': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['cdot_counting.Location']"}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        }
    }

    complete_apps = ['cdot_counting']