from django.conf.urls import patterns, include, url
from django.contrib import admin
from . import views

urlpatterns = patterns('',
    url(r'^lookup/', views.lookup, name='lookup'),
    url(r'^edit/$', views.edit, name='edit'),
    url(r'^by_page/', views.by_page, name='by_page'),
    url(r'^scrape/', views.scrape, name='scrape'),
)
