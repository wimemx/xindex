from django.conf import settings
from django.conf.urls import patterns, include, url

urlpatterns = patterns('',

    #Xindex
    url(r'^$', 'xindex.views.index', name='home'),

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


    #Reports
    url(r'^reports/', include('reports.urls')),

    #Cumulative reports
    #url(r'^cumulative_reports/', include('report_tasks.urls')),

    #Account
    url(r'^my_account/$', 'rbacx.views.my_account'),

    #Edit account
    url(r'^my_account/edit_account/(?P<data>\w+)$', 'rbacx.views.edit_account'),

    (r'^static/(?P<path>.*)$', 'django.views.static.serve',
     {'document_root': settings.STATIC_ROOT}),
    (r'^templates/media/(?P<path>.*)$', 'django.views.static.serve',
     {'document_root': settings.MEDIA_ROOT, 'show_indexes': True}),

)
