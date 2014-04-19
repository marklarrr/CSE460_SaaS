from django.conf.urls import patterns, url
from saas import views

urlpatterns = patterns('',
   url(r'^$', views.home, name='home'),
   url(r'^register/$', views.register, name='register'),
   )
  #  url(r'^category/(?P<category_name_url>\w+)/$', views.category, name='category'),)  # New!