from tastypie.resources import ModelResource
from tastypie.serializers import Serializer
from .models import Station


class StationResource(ModelResource):
    class Meta:
        queryset = Station.objects.all()
        resource_name = 'station'
        filtering = {
            'id': ('exact', ),
        }
        serializer = Serializer(formats=['json'])
