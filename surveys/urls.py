from django.conf.urls import patterns, url
from surveys import views

urlpatterns = patterns('surveys.views',

    url(r'^$', views.index, name='index'),
    url(r'order/(?P<order_type>\w+)/$', 'indexOrder'),
    url(r'^add/$', views.addSurvey, name='addSurvey'),
    url(r'^save/(?P<action>\w+)/(?P<next_step>\d+)/(?P<survey_id>\w+)',
        views.save, name='save'),
    url(r'^add/step/(?P<step>\d+)/(?P<survey_id>\d+)$',
        views.add_step, name='add_step'),
    url(r'available/(?P<survey_id>\d+)', 'available'),
    #url(r'edit/(?P<survey_id>\d+)', 'edit'),
    #url(r'remove/(?P<survey_id>\d+)', 'remove'),
    url(r'^json/$', 'getJson'),
    #url(r'details/(?P<survey_id>\d+)', 'details'),
    url(r'^media_upload/(?P<survey_id>\d+)', 'media_upload'),
    url(r'^media_upload/$', 'media_upload'),

    url(r'^(?P<survey_id>\d+)/edit/ajax/$', 'edit_ajax'),

    url(r'^save_conf/(?P<survey_id>\d+)', views.save_ajax, name='save_ajax'),
)
