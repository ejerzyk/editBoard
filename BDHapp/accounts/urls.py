from django.conf.urls import patterns, include, url
from django.contrib import admin

from . import views

urlpatterns = patterns('',
    url(r'^login/$', views.my_auth, name='login'),
    url(r'^logout/$', 'django.contrib.auth.views.logout', name='logout', kwargs={'next_page' : "/login/"}),
    url(r'new_user/$', views.new_user, name='new_user'),
    url(r'created_user/$', views.created_user, name='created_user'),
    url(r'error/$', views.error, name='error'),
    url(r'approve/$', views.approve, name='approve'),
    url(r'lookup_users/$', views.lookup_users, name='lookup_users'),
    url(r'edit_users/$', views.edit_users, name='edit_users'),
    url(r'lookup_stories/$', views.lookup_stories, name='lookup_stories'),
    url(r'edit_stories/$', views.edit_stories, name='edit_stories'),
    url(r'scrape_by_page/$', views.scrape_by_page, name='scrape_by_page'),
    url(r'by_page/$', views.by_page, name='by_page'),
    url(r'reset_password/$', views.reset_password, name='reset_password'),
    url(r'', views.home, name='home'),
)
