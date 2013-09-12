from django.conf.urls import patterns, url


urlpatterns = patterns('zones.views',

    #Companies
    url(r'^$', 'index'),
    url(r'^add/$', 'add'),
    url(r'^(?P<zone_id>\d+)/$', 'detail'),
    url(r'^(?P<zone_id>\d+)/edit/$', 'edit'),
    url(r'^(?P<zone_id>\d+)/remove/$', 'remove'),
)