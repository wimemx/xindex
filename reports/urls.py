from django.conf.urls import patterns, url
from reports import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    url(r'^moment/$', views.report_by_moment, name='report_by_moment'),
    url(r'^attribute/$', views.report_by_attribute, name='report_by_attribute'),
    url(r'^service/$', views.report_by_service, name='report_by_service'),
    url(r'^business_unit/$', views.report_by_business_unit, name='report_by_business_unit'),
    url(r'^subsidiary/$', views.report_by_subsidiary, name='report_by_subsidiary'),
    url(r'^zone/$', views.report_by_zone, name='report_by_zone'),
    url(r'^general/$', views.general_report, name='general_report'),
)