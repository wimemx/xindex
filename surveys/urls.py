from django.conf.urls import patterns, url
from surveys import views

urlpatterns = patterns('surveys.views',

    url(r'^$', views.index, name='index'),
    url(r'^add/$', views.addSurvey, name='addSurvey'),
    url(r'^add/step/(?P<step>\d+)/(?P<survey_id>\d+)$', views.add_step, name='add_step'),
    #url(r'edit/(?P<survey_id>\d+)', 'edit'),
    #url(r'remove/(?P<survey_id>\d+)', 'remove'),
    url(r'^json/$', 'getJson'),
    #url(r'details/(?P<survey_id>\d+)', 'details'),
)
