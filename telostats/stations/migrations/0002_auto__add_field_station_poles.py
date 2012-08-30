# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Station.poles'
        db.add_column('stations_station', 'poles',
                      self.gf('django.db.models.fields.IntegerField')(default=20),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'Station.poles'
        db.delete_column('stations_station', 'poles')


    models = {
        'stations.station': {
            'Meta': {'object_name': 'Station'},
            'address': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.IntegerField', [], {'unique': 'True', 'primary_key': 'True'}),
            'latitude': ('django.db.models.fields.FloatField', [], {}),
            'longitude': ('django.db.models.fields.FloatField', [], {}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'poles': ('django.db.models.fields.IntegerField', [], {})
        }
    }

    complete_apps = ['stations']