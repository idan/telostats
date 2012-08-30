from django.db import models


class Station(models.Model):
    id = models.IntegerField(unique=True, primary_key=True)
    name = models.CharField(u'name', max_length=100)
    address = models.CharField(u'address', max_length=100, null=True, blank=True)
    longitude = models.FloatField(u'longitude')
    latitude = models.FloatField(u'latitude')

    def __unicode__(self):
        return self.name
