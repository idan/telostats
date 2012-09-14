from tastypie.resources import ModelResource, Resource, Bundle, fields
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


class StationSeries():
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

    def _client(self):
        return TempoDbClient()

    def get_object_list(self, request):
        series = self._client().get_week_counts()
        return series

    def obj_get_list(self, request=None, **kwargs):
        return self.get_object_list(request)

    def obj_get(self, request=None, **kwargs):
        station_id = kwargs['pk']
        series = self._client().get_week_counts(station_id=station_id)
        station_series = StationSeries(initial=series[station_id])
        station_series.id = station_id
        return station_series

    def detail_uri_kwargs(self, bundle_or_obj):
        kwargs = {}

        if isinstance(bundle_or_obj, Bundle):
            kwargs['pk'] = bundle_or_obj.obj.uuid
        else:
            kwargs['pk'] = bundle_or_obj.uuid

        return kwargs

    class Meta:
        resource_name = 'series'
        serializer = Serializer(formats=['json'])
        allowed_methods = ['get']
