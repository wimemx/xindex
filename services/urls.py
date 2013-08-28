from django.conf.urls import patterns, include, url

urlpatterns = patterns('services.views',

    #Services
    url(r'^$', 'index'),
    url(r'^add/$', 'add'),
    #url(r'^(?P<question_id>\d+)/$', 'detail'),
    url(r'update/(?P<service_id>\d+)', 'update'),
    url(r'remove/(?P<service_id>\d+)', 'remove'),
)
