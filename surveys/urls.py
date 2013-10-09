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
    url(r'edit/(?P<survey_id>\d+)', 'edit'),
    #url(r'remove/(?P<survey_id>\d+)', 'remove'),
    url(r'^json/$', 'getJson'),
    #url(r'details/(?P<survey_id>\d+)', 'details'),
    url(r'^media_upload/(?P<survey_id>\d+)', 'media_upload'),

    #url(r'^(?P<survey_id>\d+)/edit/ajax/$', 'edit_ajax'),

    url(r'^save_conf/(?P<survey_id>\d+)', views.save_ajax, name='save_ajax'),

    #url to remove questions
    url(r'^delete_questions/', views.delete_questions, name='Delete Questions'),

    #url to remove questions
    url(r'^questions_moments/', views.associate_questions_to_moments, name='Associate Questions to Moments'),
    url(r'^questions_attributes/', views.associate_questions_to_attributes, name='Associate Questions to Attributes'),

    url(r'^add/ajax/$', 'add_ajax'),
    url(r'^preview/(?P<action>\w+)/(?P<next_step>\d+)/(?P<survey_id>\w+)',
        views.deployment, name='deployment'),

    url(r'^(?P<question_id>\d+)/edit/$', 'edit'),

    #url(r'^(?P<question_id>\d+)/remove/$', 'remove'),

    url(r'^(?P<question_id>\d+)/edit/ajax/$', 'edit_ajax'),

)
