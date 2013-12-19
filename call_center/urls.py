from django.conf.urls import patterns, include, url
from call_center import views

urlpatterns = patterns('call_center.views',

    #Call center
    url(r'^$', 'index'),

    url(r'^add/$', views.add_client),
    url(r'^search/(?P<text>\w+)$', views.getClientsInJson),

    url(r'^zone/(?P<zone_id>\d+)$', views.getZonesInJson),
    url(r'^subsidiary/(?P<subsidiary_id>\d+)$',
       views.getBusinessInJson),
    url(r'^business/(?P<business_id>\d+)$',
       views.getServicesInJson),
    url(r'^survey/(?P<business_id>\d+)/(?P<service_id>\d+)$',
       views.getSurveyInJson),

    url(r'^random/(?P<business_id>\d+)/(?P<service_id>\d+)$',
        views.getClient),
    url(r'^getsearch/(?P<client_id>\d+)/(?P<b_id>\d+)/(?P<s_id>\d+)$',
        views.getClientSearch),
)