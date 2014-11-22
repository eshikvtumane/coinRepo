from django.conf.urls import patterns, include, url
from django.contrib import admin
from users import *
from users.views import UserRegistration, UserAuth

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'coins_site.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^authentication/$', UserAuth.as_view()),
    url(r'^register/$', UserRegistration.as_view()),
)
