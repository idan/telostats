# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Station.visible'
        db.add_column('stations_station', 'visible',
                      self.gf('django.db.models.fields.BooleanField')(default=False),
                      keep_default=False)

        # but set all existing stations as visible
        for station in orm.Station.objects.all():
            station.visible = True
            station.save()


    def backwards(self, orm):
        # Deleting field 'Station.visible'
        db.delete_column('stations_station', 'visible')


    models = {
        'stations.station': {
            'Meta': {'object_name': 'Station'},
            'address': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'available': ('django.db.models.fields.IntegerField', [], {}),
            'id': ('django.db.models.fields.IntegerField', [], {'unique': 'True', 'primary_key': 'True'}),
            'latitude': ('django.db.models.fields.FloatField', [], {}),
            'longitude': ('django.db.models.fields.FloatField', [], {}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'poles': ('django.db.models.fields.IntegerField', [], {}),
            'polygon': ('jsonfield.fields.JSONField', [], {'default': '{}'}),
            'visible': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        }
    }

    complete_apps = ['stations']