from django.conf.urls import patterns, url
from indicators import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    url(r'^(?P<indicator_id>\d+)/$', views.detail, name='detail'),
    url(r'^add/$', views.add, name='add'),
)
