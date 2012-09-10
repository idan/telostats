from django.conf.urls import patterns, include, url
from django.contrib import admin
from tastypie.api import Api
from telostats.stations.api import StationResource, SeriesResource

admin.autodiscover()

v1_api = Api(api_name='v1')
v1_api.register(StationResource())
v1_api.register(SeriesResource())

urlpatterns = patterns('',
    url(r'^', include('telostats.stations.urls')),
    url(r'^api/', include(v1_api.urls)),
    url(r'^admin/', include(admin.site.urls)),
)
