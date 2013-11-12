from django.conf.urls import patterns, include, url

urlpatterns = patterns('subsidiaries.views',

    #Subsidiaries
    url(r'^$', 'index'),
    url(r'^add/$', 'add'),

    #pruebas
    #url(r'^new/$', 'new'),
    url(r'^add/$', 'add'),
    #fin pruebas
    #url(r'^(?P<question_id>\d+)/$', 'detail'),
    url(r'edit/(?P<subsidiary_id>\d+)', 'edit'),
    url(r'remove/(?P<subsidiary_id>\d+)', 'remove'),

    #test
    url(r'^json/$', 'getSubsidiariesInJson'),
    url(r'details/(?P<subsidiary_id>\d+)', 'details'),
    url(r'sub_by_city/$', 'getSubsidiariesByCity'),

    #Url to get subsidiaries
    url(r'^get_business_units/$', 'get_business_units'),
)
