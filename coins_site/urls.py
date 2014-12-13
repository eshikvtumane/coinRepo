from django.conf.urls import patterns, include, url
from django.contrib import admin
#import django.contrib.staticfiles.views
#from users import *
#from coins import *

urlpatterns = patterns('',
    # Examples:
    url(r'^grappelli/', include('grappelli.urls')),
    url(r'^', include('main.urls')),
    url(r'^coins/',include('coins.urls')),
    url(r'^users/', include('users.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^search/', include('haystack.urls')),
)
