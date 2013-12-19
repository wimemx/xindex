from django.conf.urls import patterns, url


urlpatterns = patterns('companies.views',

    #Companies
    url(r'^$', 'index'),
    url(r'^add/$', 'add'),
    url(r'^(?P<company_id>\d+)/$', 'detail'),
    url(r'^(?P<company_id>\d+)/edit/$', 'edit'),
    url(r'^(?P<company_id>\d+)/remove/$', 'remove'),

    #test
    url(r'^json/$', 'getCInJson'),
    url(r'^(?P<company_id>\d+)/details/$', 'details'),
    #url to edit the privacy notice
    url(r'^privacy_notice/$', 'edit_privacy_notice'),
    #url to edit the email template
    url(r'^email_template/$', 'edit_email_template'),
    #url to upload company logo
    url(r'^upload_logo/(?P<company_id>\d+)/$', 'upload_logo'),

)