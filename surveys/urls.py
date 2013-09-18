from django.conf.urls import patterns, url
from indicators import views

urlpatterns = patterns('surveys.views',

    url(r'^$', views.index, name='index'),
    #url(r'^(?P<indicator_id>\d+)/$', views.detail, name='detail'),
    url(r'^add/$', views.add, name='add'),
    url(r'edit/(?P<survey_id>\d+)', 'edit'),
    url(r'remove/(?P<survey_id>\d+)', 'remove'),
    url(r'^json/$', 'getJson'),
    url(r'details/(?P<survey_id>\d+)', 'details'),
)
