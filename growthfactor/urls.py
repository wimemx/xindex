from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'growthfactor.views.home', name='home'),
    # url(r'^growthfactor/', include('growthfactor.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),

    #Moments
    url(r'^moments/', include('moments.urls')),

    #Owners
    url(r'^owners/', include('owners.urls')),

    #Attributes
    #url(r'^attributes/', include('attributes.urls')),

    #Attributes
    url(r'^indicators/', include('indicators.urls')),

    #Questions
    url(r'^questions/', include('questions.urls')),

    #Subsidiaries
    url(r'^subsidiaries/', include('subsidiaries.urls')),

    #Subsidiary types
    url(r'^subsidiary_types/', include('subsidiary_types.urls')),

    #Business unit
    url(r'^business_units/', include('business_units.urls')),

    #Services
    url(r'^services/', include('services.urls')),


    #Index
    url(r'^xindex/$', 'xindex.views.index'),

    #Companies
    url(r'^companies/', include('companies.urls')),

    #Zones
    url(r'^zones/', include('zones.urls')),

    #Company_types
    url(r'^company_types/', include('company_types.urls')),

     #Surveys
    url(r'^surveys/', include('surveys.urls')),
)
