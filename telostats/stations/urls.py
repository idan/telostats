from django.conf.urls import patterns, url

from .views import About, AboutApi, Contact, StationMap, StationDetail

urlpatterns = patterns('',

    url('^$', StationMap.as_view(), name='home'),
    url('^about$', About.as_view(), name='about'),
    url('^about/api$', AboutApi.as_view(), name='about_api'),
    url('^contact$', Contact.as_view(), name='contact'),
    url('^station/(?P<pk>\d+)', StationDetail.as_view(), name='station_detail'),
)
