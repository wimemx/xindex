from django.conf.urls import patterns, url
from clients import views

urlpatterns = patterns('clients.views',
                       url(r'^$', views.client_list),
                       url(r'^add/$', views.add_client),
                       url(r'^remove/(?P<client_id>\d+)$', views.remove_client),
                       url(r'^edit/(?P<client_id>\d+)$', views.edit_client),
                       url(r'^json/$', views.getClientsInJson),
                       )
