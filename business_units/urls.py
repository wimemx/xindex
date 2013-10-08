from django.conf.urls import patterns, include, url

urlpatterns = patterns('business_units.views',

    #Business units
    url(r'^$', 'index'),
    url(r'^add/$', 'add'),
    url(r'update/(?P<business_unit_id>\d+)', 'update'),
    #url(r'remove/(?P<business_unit_id>\d+)', 'remove'),
    url(r'^(?P<subsidiary_id>\d+)/(?P<business_unit_id>\d+)/remove/$',
        'remove'),
    url(r'^json/$', 'getBUInJson'),
    url(r'details/(?P<business_unit_id>\d+)', 'details'),
)
