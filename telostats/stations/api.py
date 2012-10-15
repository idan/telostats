import json

from tastypie.resources import ModelResource, Resource, fields
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
        excludes = ['visible']

    def dehydrate(self, bundle):
        bundle.data['polygon'] = json.loads(bundle.data['polygon'])
        return bundle


class StationSeries:
    def __init__(self, initial=None):
        self.__dict__['_data'] = {}

        if hasattr(initial, 'items'):
            self.__dict__['_data'] = initial

    def __getattr__(self, name):
        return self._data.get(name, None)

    def __setattr__(self, name, value):
        self.__dict__['_data'][name] = value

    def to_dict(self):
        return self._data


class SeriesResource(Resource):
    id = fields.CharField(attribute='id')
    poles = fields.ListField(attribute='poles')
    available = fields.ListField(attribute='available')

    class Meta:
        object_class = StationSeries
        resource_name = 'series'
        serializer = Serializer(formats=['json'])
        limit = 200
        allowed_methods = ['get']
        filtering = {
            'id': ('exact', ),
        }

    def _client(self):
        return TempoDbClient()

    def _get_series(self, station_id=None, **kwargs):
        return self._client().get_series(station_id, **kwargs)

    def get_object_list(self, request):
        series_list = self._get_series(hours=2).items()
        res = []
        for sta_id, series in series_list:
            obj = StationSeries(initial=series)
            obj.id = sta_id
            res.append(obj)
        return res

    def obj_get_list(self, request=None, **kwargs):
        return self.get_object_list(request)

    def obj_get(self, request=None, **kwargs):
        station_id = kwargs['pk']
        series = self._get_series(station_id=station_id, hours=2)
        station_series = StationSeries(initial=series[station_id])
        station_series.id = station_id
        return station_series
