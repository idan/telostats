from tastypie.resources import ModelResource, Resource
from tastypie.serializers import Serializer
from .models import Station
from ..utils.tempodb import TempoDbClient


class StationResource(ModelResource):
    class Meta:
        queryset = Station.objects.all()
        resource_name = 'station'
        serializer = Serializer(formats=['json'])
        limit = 200  # show all stations by default
        allowed_methods = ['get']
        filtering = {
            'id': ('exact', ),
        }


class SeriesResource(Resource):

    def _client(self):
        return TempoDbClient()

    def get_object_list(self, request):
        series = self._client().get_week_counts()
        return series

    def obj_get_list(self, request=None, **kwargs):
        return self.get_object_list(request)

    class Meta:
        resource_name = 'series'
        serializer = Serializer(formats=['json'])
        allowed_methods = ['get']
