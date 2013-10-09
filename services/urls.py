from django.conf.urls import patterns, include, url

urlpatterns = patterns('services.views',

    #Services
    url(r'^$', 'index'),
    url(r'^(?P<business_unit_id>\d+)', 'index'),
    url(r'^add/(?P<business_unit_id>\d+)', 'add'),
    #url(r'^(?P<question_id>\d+)/$', 'detail'),
    url(r'update/(?P<service_id>\d+)/(?P<business_unit_id>\d+)', 'update'),
    url(r'remove/(?P<service_id>\d+)/(?P<business_unit_id>\d+)', 'remove'),

    #test
    url(r'^json/$', 'getSInJson'),
    url(r'^json/(?P<business_unit_id>\d+)$', 'getSByBUInJson'),
    url(r'details/(?P<service_id>\d+)', 'details'),
)
