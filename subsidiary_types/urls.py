from django.conf.urls import patterns, url

urlpatterns = patterns('subsidiary_types.views',

    #Subsidiary types
    url(r'^$', 'index'),
    url(r'^add/$', 'add'),
    url(r'update/(?P<subsidiary_type_id>\d+)', 'update'),
    url(r'remove/(?P<subsidiary_type_id>\d+)', 'remove'),
    url(r'^json/$', 'getSTInJson'),
    url(r'details/(?P<subsidiary_type_id>\d+)', 'details'),
    url(r'subsidiary_types/', 'stByCompany'),
)
