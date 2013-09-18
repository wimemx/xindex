from django.conf.urls import patterns, include, url

urlpatterns = patterns('subsidiary_types.views',

    #Subsidiary types
    url(r'^$', 'index'),
    url(r'^add/$', 'add'),

    #url(r'^(?P<question_id>\d+)/$', 'detail'),
    url(r'update/(?P<subsidiary_type_id>\d+)', 'update'),
    url(r'remove/(?P<subsidiary_type_id>\d+)', 'remove'),

    url(r'^json/$', 'getSTInJson'),
    #url(r'^tipos_subsidiarias/$', 'tipos_subsidiarias'),
    url(r'details/(?P<subsidiary_type_id>\d+)', 'details'),
    url(r'subsidiary_types/', 'stByCompany'),
)
