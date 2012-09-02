from django.conf.urls import patterns, url

from .views import StationMap, StationList, StationDetail

urlpatterns = patterns('',

    url('^$', StationList.as_view(), name='station_list'),
    url('^station/(?P<pk>\d+)', StationDetail.as_view(), name='station_detail'),
    url('^map', StationMap.as_view(), name='station_map')
)
