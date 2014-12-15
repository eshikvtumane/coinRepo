from django.conf.urls import patterns, include, url
from django.contrib import admin
from users import *
from users.views import UserRegistration, UserAuth, UserLogout, UserInfo, UserCountry

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'coins_site.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^authentication/$', UserAuth.as_view()),
    url(r'^register/$', UserRegistration.as_view()),
    url(r'^logout/$', UserLogout.as_view()),
    url(r'^info/$', UserInfo.as_view()),

    #for collections
    url(r'^collections/', UserCountry.as_view()),
    url(r'^ajax/add/country/$', UserCountry.as_view()),
)
