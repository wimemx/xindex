from django.conf.urls import patterns, url
from moments import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    url(r'^add/$', views.add, name='add'),
    url(r'^(?P<moment_id>\d+)/$', views.detail, name='detail'),
    url(r'^(?P<moment_id>\d+)/edit/$', views.edit, name='edit'),
)