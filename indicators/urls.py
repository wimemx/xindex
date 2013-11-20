from django.conf.urls import patterns, url
from indicators import views

urlpatterns = patterns('indicators.views',

    url(r'^$', views.index, name='index'),
    url(r'^add/$', views.add, name='add'),
    url(r'update/(?P<indicator_id>\d+)', 'update'),
    url(r'remove/(?P<indicator_id>\d+)', 'remove'),
    url(r'^json/$', 'getSInJson'),
    url(r'details/(?P<indicator_id>\d+)', 'details'),
)
