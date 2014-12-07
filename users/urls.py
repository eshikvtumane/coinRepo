from django.conf.urls import patterns, include, url
from django.contrib import admin
from users import *
from users.views import UserRegistration, UserAuth, UserLogout, UserProfile

urlpatterns = patterns('',

    url(r'^authentication/$', UserAuth.as_view()),
    url(r'^register/$', UserRegistration.as_view()),
    url(r'^logout/$', UserLogout.as_view()),
    url(r'^profile/$', UserProfile.as_view())
)
