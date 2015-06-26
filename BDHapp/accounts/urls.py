from django.conf.urls import patterns, include, url
from django.contrib import admin

from . import views

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'BDHapp.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^login/$', views.my_auth, name='login'),
    url(r'^logout/$', 'django.contrib.auth.views.logout', name='logout', kwargs={'next_page' : '/login/'}),
    url(r'new_user/$', views.new_user, name='new_user'),
    url(r'created_user/$', views.created_user, name='created_user'),
    url(r'error/$', views.error, name='error'),
    url(r'approve/$', views.approve, name='approve'),
    url(r'lookup/$', views.lookup, name='lookup'),
    url(r'', views.home, name='home'),
)
