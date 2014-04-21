from django.conf.urls import patterns, include, url
from saas import views
from django.contrib import admin
from django.conf import settings

admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'tango_with_django_project.views.home', name='home'),
    # url(r'^tango_with_django_project/', include('tango_with_django_project.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
     url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
	url(r'^saas/register/$', views.register, name='register'),# ADD THIS NEW TUPLE!
    url(r'^saas/login/$', views.user_login, name='login'),
    url(r'^saas/addProject/$', views.addProject, name='addProject'),
    url(r'^saas/addRequirement/$', views.addRequirement, name='addRequirement'),
    url(r'^saas/addManager/$', views.addManager, name='addManager'),
    url(r'^saas/addWorker/$', views.addWorker, name='addWorker'),
    url(r'^saas/Tenanthome/$', views.tenantHome, name='Tenanthome'),
    url(r'^saas/logout/$', views.user_logout, name='logout'),
    url(r'^saas/websitehomepage/$', views.index, name='home'),
    url(r'^saas/ManagerLogin/$', views.manager_login, name='ManagerLogin'),
    url(r'^saas/WorkerLogin/$', views.worker_login, name='WorkerLogin'),
    url(r'^saas/Dashboard/$', views.Dashboard, name='Dashboard'),
    url(r'^saas/workerHome/$', views.workerHome, name='workerHome'),
    url(r'^saas/viewAssignedRequirements/$', views.viewRequirements, name='viewRequirements'),
    url(r'^saas/viewManagerProjects/$', views.viewProjectsAddedByManager, name='viewManagerProjects'),
    url(r'^saas/viewAllProjects/$', views.viewAllTenantProjects, name='viewAllProjects'),
)
'''
if settings.DEBUG:
    urlpatterns += patterns(
        'django.views.static',
        (r'media/(?P<path>.*)',
        'serve',
        {'document_root': settings.MEDIA_ROOT}),)
'''