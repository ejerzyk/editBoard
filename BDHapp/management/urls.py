from django.conf.urls import patterns, include, url
from . import views 

urlpatterns = patterns('',
    url(r'^select/$', views.select, name='select'),
    url(r'^report/$', views.report, name='report'),
)