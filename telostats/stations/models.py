from django.db import models
from django.utils import timezone


class Station(models.Model):
    id = models.IntegerField(unique=True, primary_key=True)
    name = models.CharField(u'name', max_length=100)
    longitude = models.FloatField(u'longitude')
    latitude = models.FloatField(u'latitude')


class Status(models.Model):
    station = models.ForeignKey(Station)
    timestamp = models.DateTimeField(default=timezone.now)
    actual_timestamp = models.DateTimeField(default=timezone.now)
    bikes = models.IntegerField(u'available bikes')
    docks = models.IntegerField(u'available docks')
