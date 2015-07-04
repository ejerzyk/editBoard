from django.conf.urls import patterns, include, url
from django.contrib import admin


# import management, stories, accounts, students

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'BDHapp.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^management/', include('management.urls', namespace='management')),
    url(r'^accounts/', include('accounts.urls', namespace='accounts')),
    url(r'^students/',include('students.urls', namespace='students')),
    url(r'', include('accounts.urls', namespace='accounts')),
)
