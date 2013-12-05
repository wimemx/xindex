from django.conf.urls import patterns, url
from clients import views

urlpatterns = patterns('clients.views',
                       url(r'^$', views.client_list),
                       url(r'^add/$', views.add_client),
                       url(r'^remove/(?P<client_id>\d+)$', views.remove_client),
                       url(r'^edit/(?P<client_id>\d+)$', views.edit_client),
                       url(r'^json/$', views.getClientsInJson),
                       url(r'^csv/$', views.csv_read),
                       url(r'^details/(?P<client_id>\d+)$',
                           views.getAnswersByClient),
                       url(r'^activity/(?P<client_id>\d+)$',
                           views.getClientActivityInJson),
                       url(r'^zone/(?P<zone_id>\d+)$',
                           views.getZonesInJson),
                       url(r'^subsidiary/(?P<subsidiary_id>\d+)$',
                           views.getBusinessInJson),
                       url(r'^business/(?P<business_id>\d+)$',
                           views.getServicesInJson),
                       )
