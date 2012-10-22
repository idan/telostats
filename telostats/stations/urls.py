from django.conf.urls import patterns, url

from .views import About, StationMap, StationDetail

urlpatterns = patterns('',

    url('^$', StationMap.as_view(), name='home'),
    url('^about$', About.as_view(), name='about'),
    url('^station/(?P<pk>\d+)', StationDetail.as_view(), name='station_detail'),
)
