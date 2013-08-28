from django.conf.urls import patterns, url
from owners import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    url(r'^(?P<owner_id>\d+)/$', views.detail, name='detail'),
    url(r'^add$', views.add, name='add'),
    url(r'^(?P<owner_id>\d+)/edit/$', views.edit, name='edit'),
)