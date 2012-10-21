from django.conf.urls import patterns, url

from .views import StationMap, StationDetail

urlpatterns = patterns('',

    url('^$', StationMap.as_view(), name='station_map'),
    url('^station/(?P<pk>\d+)', StationDetail.as_view(), name='station_detail'),
)
