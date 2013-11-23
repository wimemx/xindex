from django.conf.urls import patterns, url

urlpatterns = patterns('subsidiaries.views',

    #Subsidiaries
    url(r'^$', 'index'),
    url(r'^add/$', 'add'),
    url(r'^add/$', 'add'),
    url(r'edit/(?P<subsidiary_id>\d+)', 'edit'),
    url(r'remove/(?P<subsidiary_id>\d+)', 'remove'),
    url(r'^json/$', 'getSubsidiariesInJson'),
    url(r'details/json/(?P<subsidiary_id>\d+)', 'getSubsidiaryDetailsInJson'),
    url(r'details/(?P<subsidiary_id>\d+)', 'details'),

    #Url to get business units
    url(r'^get_business_units/$', 'get_business_units'),
)
