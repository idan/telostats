# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Station'
        db.create_table('stations_station', (
            ('id', self.gf('django.db.models.fields.IntegerField')(unique=True, primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('longitude', self.gf('django.db.models.fields.FloatField')()),
            ('latitude', self.gf('django.db.models.fields.FloatField')()),
        ))
        db.send_create_signal('stations', ['Station'])

        # Adding model 'Status'
        db.create_table('stations_status', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('station', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['stations.Station'])),
            ('timestamp', self.gf('django.db.models.fields.DateTimeField')()),
            ('bikes', self.gf('django.db.models.fields.IntegerField')()),
            ('docks', self.gf('django.db.models.fields.IntegerField')()),
        ))
        db.send_create_signal('stations', ['Status'])


    def backwards(self, orm):
        # Deleting model 'Station'
        db.delete_table('stations_station')

        # Deleting model 'Status'
        db.delete_table('stations_status')


    models = {
        'stations.station': {
            'Meta': {'object_name': 'Station'},
            'id': ('django.db.models.fields.IntegerField', [], {'unique': 'True', 'primary_key': 'True'}),
            'latitude': ('django.db.models.fields.FloatField', [], {}),
            'longitude': ('django.db.models.fields.FloatField', [], {}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'stations.status': {
            'Meta': {'object_name': 'Status'},
            'bikes': ('django.db.models.fields.IntegerField', [], {}),
            'docks': ('django.db.models.fields.IntegerField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'station': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['stations.Station']"}),
            'timestamp': ('django.db.models.fields.DateTimeField', [], {})
        }
    }

    complete_apps = ['stations']