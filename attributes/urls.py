from django.conf.urls import patterns, url
from attributes import views

urlpatterns = patterns('',
    url(r'^$', views.index, name="index"),
    url(r'^(?P<attribute_id>\d+)/$', views.detail, name="detail"),
    url(r'^add/$', views.add, name="add"),
    url(r'^(?P<attribute_id>\d+)/edit/$', views.edit, name='edit'),
)