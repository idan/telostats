from django.db import models
from jsonfield import JSONField


class VisibleStationManager(models.Manager):
    def get_query_set(self):
        return super(VisibleStationManager, self).get_query_set().filter(visible=True)


class Station(models.Model):
    id = models.IntegerField(unique=True, primary_key=True)
    name = models.CharField(u'name', max_length=100)
    address = models.CharField(u'address', max_length=100, null=True, blank=True)
    longitude = models.FloatField(u'longitude')
    latitude = models.FloatField(u'latitude')
    polygon = JSONField(u'polygon')
    poles = models.IntegerField(u'poles')
    available = models.IntegerField(u'available')
    visible = models.BooleanField(u'visible', default=False)

    objects = models.Manager()
    visible_objects = VisibleStationManager()

    def __unicode__(self):
        return u'({}) {}'.format(self.id, self.name)

    def available_poles(self):
        return self.available

    def available_bikes(self):
        return self.poles - self.available
