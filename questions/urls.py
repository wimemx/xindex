from django.conf.urls import patterns, include, url

urlpatterns = patterns('questions.views',

    #Questions
    url(r'^$', 'index'),
    url(r'^add/$', 'add'),
    url(r'^add/ajax/$', 'add_ajax'),
    url(r'^(?P<question_id>\d+)/$', 'detail'),
    url(r'^(?P<question_id>\d+)/edit/$', 'edit'),
    url(r'^(?P<question_id>\d+)/edit/ajax/$', 'edit_ajax'),
    url(r'^(?P<question_id>\d+)/remove/$', 'remove'),
)
