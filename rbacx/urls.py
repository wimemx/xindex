from django.conf.urls import patterns, url

urlpatterns = patterns('rbacx.views',

    #Profile
    url(r'^$', 'profile'),
)