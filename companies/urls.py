from django.conf.urls import patterns, url


urlpatterns = patterns('companies.views',

    #Companies
    url(r'^$', 'index'),
    url(r'^add/$', 'add'),
    url(r'^(?P<company_id>\d+)/$', 'detail'),
    url(r'^(?P<company_id>\d+)/edit/$', 'edit'),
    url(r'^(?P<company_id>\d+)/remove/$', 'remove'),
)