from django.conf.urls import patterns, url


urlpatterns = patterns('zones.views',

    #Zones
    url(r'^$', 'index'),
    url(r'^add/$', 'add'),
    url(r'^add_state/(?P<zone_id>\d+)/$', 'add_state'),
    url(r'^(?P<zone_id>\d+)/$', 'detail'),
    url(r'^(?P<zone_id>\d+)/edit/$', 'edit'),
    url(r'^(?P<zone_id>\d+)/remove/$', 'remove'),
    url(r'^json/$', 'getZonesInJson'),
    url(r'^country/(?P<country_id>\d+)/$', 'country'),
    url(r'^get_subsidiaries/$', 'get_subsidiaries'),
)