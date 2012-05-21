from tastypie import fields
from tastypie.resources import ModelResource
from .models import Station, Status

class StationResource(ModelResource):
    class Meta:
        queryset = Station.objects.all()
        resource_name = 'station'

class StatusResource(ModelResource):
    station = fields.ForeignKey(StationResource, 'station')
    class Meta:
        queryset = Status.objects.all()
        resource_name = 'status'
        excludes = ['actual_timestamp', 'id']
        filtering = {
            'station': ('exact',),
            'timestamp': ('gt', 'gte', 'lt', 'lte', 'range',
                          'year', 'month', 'day', 'week_day')
        }
