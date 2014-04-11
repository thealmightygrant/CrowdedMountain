# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding M2M table for field add_segments on 'Resort'
        m2m_table_name = db.shorten_name(u'cdot_counting_resort_add_segments')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('resort', models.ForeignKey(orm[u'cdot_counting.resort'], null=False)),
            ('highwaysegment', models.ForeignKey(orm[u'cdot_counting.highwaysegment'], null=False))
        ))
        db.create_unique(m2m_table_name, ['resort_id', 'highwaysegment_id'])

        # Adding M2M table for field sub_segments on 'Resort'
        m2m_table_name = db.shorten_name(u'cdot_counting_resort_sub_segments')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('resort', models.ForeignKey(orm[u'cdot_counting.resort'], null=False)),
            ('highwaysegment', models.ForeignKey(orm[u'cdot_counting.highwaysegment'], null=False))
        ))
        db.create_unique(m2m_table_name, ['resort_id', 'highwaysegment_id'])

        # Deleting field 'HighwaySegment.name'
        db.delete_column(u'cdot_counting_highwaysegment', 'name')

        # Adding field 'HighwaySegment.highway_name'
        db.add_column(u'cdot_counting_highwaysegment', 'highway_name',
                      self.gf('django.db.models.fields.CharField')(default='none', max_length=20),
                      keep_default=False)


    def backwards(self, orm):
        # Removing M2M table for field add_segments on 'Resort'
        db.delete_table(db.shorten_name(u'cdot_counting_resort_add_segments'))

        # Removing M2M table for field sub_segments on 'Resort'
        db.delete_table(db.shorten_name(u'cdot_counting_resort_sub_segments'))

        # Adding field 'HighwaySegment.name'
        db.add_column(u'cdot_counting_highwaysegment', 'name',
                      self.gf('django.db.models.fields.CharField')(default='none', max_length=20),
                      keep_default=False)

        # Deleting field 'HighwaySegment.highway_name'
        db.delete_column(u'cdot_counting_highwaysegment', 'highway_name')


    models = {
        u'cdot_counting.countstatistic': {
            'Meta': {'ordering': "['resort', 'date']", 'object_name': 'CountStatistic'},
            'count': ('django.db.models.fields.IntegerField', [], {}),
            'date': ('django.db.models.fields.DateTimeField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'resort': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['cdot_counting.Resort']"})
        },
        u'cdot_counting.highwaysegment': {
            'Meta': {'ordering': "['highway_name', 'datetime_calculated']", 'object_name': 'HighwaySegment'},
            'avg_occupancy': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'avg_volume': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'current_travel_time': ('django.db.models.fields.IntegerField', [], {}),
            'datetime_calculated': ('django.db.models.fields.DateTimeField', [], {}),
            'direction': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'end_mile_marker': ('django.db.models.fields.DecimalField', [], {'max_digits': '8', 'decimal_places': '2'}),
            'expected_travel_time': ('django.db.models.fields.IntegerField', [], {}),
            'highway_name': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
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
            'add_segments': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'add_segments'", 'symmetrical': 'False', 'to': u"orm['cdot_counting.HighwaySegment']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'location': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['cdot_counting.Location']"}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'sub_segments': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'sub_segments'", 'symmetrical': 'False', 'to': u"orm['cdot_counting.HighwaySegment']"})
        }
    }

    complete_apps = ['cdot_counting']