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
    url(r'^delete_questions/', views.delete_questions,
        name='Delete Questions'),

    #url to check if a survey has blocks style and return it if so
    url(r'^getSurveyBlocksStyle/', views.get_survey_blocks_style,
        name='Get survey blocks style'),

    #url to remove questions
    url(r'^questions_moments/', views.associate_questions_to_moments,
        name='Associate Questions to Moments'),
    #url(r'^questions_attributes/', views.associate_questions_to_attributes,
     #   name='Associate Questions to Attributes'),

    url(r'^add/ajax/$', 'add_ajax'),
    url(r'^preview/(?P<action>\w+)/(?P<next_step>\d+)/(?P<survey_id>\w+)',
        views.deployment, name='deployment'),

    #url to get question data to edit
    url(r'^(?P<question_id>\d+)/edit/$', 'get_question_data_to_update'),

    #url(r'^(?P<question_id>\d+)/remove/$', 'remove'),

    url(r'^(?P<question_id>\d+)/edit/ajax/$', 'edit_ajax'),

    #url to show a survey
    url(r'^answer/(?P<survey_id_encoded>\w+)/(?P<hash_code>\w+)/(?P<client_id_encoded>\w+)/$',
        'answer_survey'),

    #url to save the answers
    url(r'^save_answers/$', 'save_answers_ajax'),

)
