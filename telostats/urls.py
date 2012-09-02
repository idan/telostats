from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

from tastypie.api import Api
v1_api = Api(api_name='v1')

from telostats.stations.api import StationResource
v1_api.register(StationResource())

urlpatterns = patterns('',
    # url(r'^', include('telostats.stations.urls')),
    url(r'^api/', include(v1_api.urls)),
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^admin/', include(admin.site.urls)),
)
