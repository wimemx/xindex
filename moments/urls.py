from django.conf.urls import patterns, url
from moments import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    url(r'^add/(?P<service_id>\d)', views.add, name='add'),
    url(r'^(?P<moment_id>\d+)/$', views.detail, name='detail'),
    url(r'^(?P<moment_id>\d+)/edit/$', views.edit, name='edit'),
    url(r'^(?P<service_id>\d+)/(?P<moment_id>\d+)/remove/$',
        views.remove, name='remove'),
    #Url to get the attributes
    url(r'^get_attributes/$', views.get_attributes),
)