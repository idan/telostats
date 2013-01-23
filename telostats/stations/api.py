import json

from datetime import datetime, timedelta
from dateutil.parser import parse as parse_date
from tastypie.cache import SimpleCache
from tastypie.resources import ModelResource, Resource, fields
from tastypie.serializers import Serializer
from .models import Station
from ..utils.tempodb import TempoDbClient


class StationResource(ModelResource):
    class Meta:
        queryset = Station.visible_objects.all()
        resource_name = 'station'
        serializer = Serializer(formats=['json'])
        limit = 0  # show all stations by default
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


class RecentResource(Resource):
    id = fields.CharField(attribute='id')
    series = fields.ListField(attribute='series')

    class Meta:
        object_class = StationSeries
        resource_name = 'recent'
        # cache = SimpleCache(timeout=60 * 60)
        serializer = Serializer(formats=['json'])
        limit = 1
        list_allowed_methods = []
        detail_allowed_methods = ['get']
        filtering = {
            'id': ('exact', ),
        }

    def _client(self):
        return TempoDbClient()

    def _get_series(self, station_id=None, **kwargs):
        return self._client().get_series(station_id, **kwargs)

    def get_object_list(self, request):
        series_list = self._get_series().items()
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
        series = self._get_series(station_id=station_id)[station_id]
        # zip the two lists together on same timestamps
        timestamps = [x['t'] for x in series['available']]  # or poles, dm;st
        available = [x['v'] for x in series['available']]
        poles = [x['v'] for x in series['poles']]
        series = [{
            'timestamp': t,
            'poles': p,
            'available': a,
            'bikes': p - a
        } for t, p, a in zip(timestamps, poles, available)]
        initial_series = {'series': series}
        station_series = StationSeries(initial=initial_series)
        station_series.id = station_id
        return station_series


class AverageResource(Resource):
    id = fields.CharField(attribute='id')
    series = fields.ListField(attribute='series')

    class Meta:
        object_class = StationSeries
        resource_name = 'average'
        # cache = SimpleCache(timeout=60 * 60 * 24 * 7)
        serializer = Serializer(formats=['json'])
        limit = 1
        list_allowed_methods = []
        detail_allowed_methods = ['get']
        filtering = {
            'id': ('exact', ),
        }

    def _client(self):
        return TempoDbClient()

    def _get_series(self, station_id=None, **kwargs):
        return self._client().get_series(station_id, start=timedelta(days=7), **kwargs)

    def obj_get(self, request=None, **kwargs):
        station_id = kwargs['pk']
        series = self._get_series(station_id=station_id)[station_id]

        # initial result structure
        res = dict([
            (i, {'available': [], 'poles': []})
        for i in range(24)])

        # data collection in buckets
        for s in ['available', 'poles']:
            for datum in series[s]:
                hour = parse_date(datum['t']).hour
                res[hour][s].append(datum['v'])

        # reduce lists by average
        res = [{
            'timestamp': datetime(2013, 1, 1, k).isoformat(),
            'available': sum(v['available']) / len(v['available']),
            'poles': sum(v['poles']) / len(v['poles']),
        } for k, v in res.items()]

        # add final bike count
        for hour in res:
            hour['bikes'] = hour['poles'] - hour['available']

        initial_series = {'series': res}
        station_series = StationSeries(initial=initial_series)
        station_series.id = station_id
        return station_series
