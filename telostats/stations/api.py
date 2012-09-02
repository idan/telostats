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

    def dehydrate(self, bundle):
        station_id = str(bundle.data['id'])
        counts = get_latest_counts(station_id)
        bundle.data['available'] = counts[station_id]['available']
        bundle.data['poles'] = counts[station_id]['poles']
        return bundle
