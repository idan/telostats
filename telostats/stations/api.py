from tastypie.resources import ModelResource
from tastypie.serializers import Serializer
from .models import Station
from ..utils.tempodb import get_latest_counts


class StationResource(ModelResource):
    class Meta:
        queryset = Station.objects.all()
        resource_name = 'station'
        serializer = Serializer(formats=['json'])
        limit = 200  # show all stations by default
        filtering = {
            'id': ('exact', ),
        }

    def alter_list_data_to_serialize(self, request, data):
        # we're using this method as a hook before the data is serialized back
        # to the client, that is only called once per call (as opposed to hydrate()
        # which is called per each object), to inject the availability data
        counts = get_latest_counts()
        for bundle in data['objects']:
            station_id = str(bundle.data['id'])
            bundle.data['available'] = counts[station_id]['available']
            bundle.data['poles'] = counts[station_id]['poles']
        return data
