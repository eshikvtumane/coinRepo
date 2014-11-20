from django.conf.urls import patterns, include, url
from django.contrib import admin
from users import *

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'coins_site.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^user/', include('users.urls')),
)
