from django.conf.urls import patterns, include, url
from django.contrib import admin

from . import views

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'BDHapp.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^lookup/$', views.lookup, name='lookup'),
    url(r'^edit/$', views.edit, name='edit'),
)
