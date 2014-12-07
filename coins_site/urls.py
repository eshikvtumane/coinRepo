from django.conf.urls import patterns, include, url
from django.contrib import admin
#from users import *
#from coins import *

urlpatterns = patterns('',
    url(r'^coins/',include('coins.urls')),
    url(r'^users/', include('users.urls')),
    url(r'^admin/', include(admin.site.urls)),
)
