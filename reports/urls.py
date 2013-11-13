from django.conf.urls import patterns, url
from reports import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    url(r'^moment/$', views.report_by_moment, name='report_by_moment'),
    url(r'^attribute/$', views.report_by_attribute, name='report_by_attribute'),
)