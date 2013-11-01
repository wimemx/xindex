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
    url(r'^surveys/', include('clients.urls')),

    #Clients
    url(r'^clients/', include('clients.urls')),

    #Surveys_search
    url(r'^search/$', 'xindex.views.search'),

    #Signin
    url(r'^signin/$', 'xindex.views.signin'),

    #Signup
    url(r'^signup/$', 'xindex.views.signup'),

    #Login
    url(r'^login/$', 'xindex.views.login'),

    #Logout
    url(r'^logout/$', 'xindex.views.log_out'),

    #Profile
    url(r'^profile/$', include('rbacx.urls')),

    #Profile Edit
    url(r'^profile/edit/(?P<action>\d+)$', 'rbacx.views.edit_profile'),

    #Control Panel
    url(r'^control_panel/$', 'rbacx.views.control_panel'),

    #User List
    url(r'^user_list/$', 'rbacx.views.user_list'),

    #User List
    url(r'^user_list/json/$', 'rbacx.views.getUsersInJson'),

    #Add User
    url(r'^user/add/$', 'rbacx.views.create_user'),

    #Edit User
    url(r'^user/edit/(?P<user_id>\d+)$', 'rbacx.views.edit_user'),

    #Delete User
    url(r'^user/delete/(?P<user_id>\d+)$', 'rbacx.views.delete_user'),

)
