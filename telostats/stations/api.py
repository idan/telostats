from tastypie.resources import ModelResource
from tastypie.serializers import Serializer
from .models import Station


class StationResource(ModelResource):
    class Meta:
        queryset = Station.objects.all()
        resource_name = 'station'
        serializer = Serializer(formats=['json'])
        limit = 200  # show all stations by default
        filtering = {
            'id': ('exact', ),
        }
