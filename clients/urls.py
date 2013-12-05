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
                       url(r'^activity_answers/(?P<activity_id>\d+)$',
                           views.activity_answers),
                       )
