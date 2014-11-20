from django.conf.urls import patterns, include, url
from django.contrib import admin
from users import *
from users.views import RegistrationForm

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'coins_site.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^user/', RegistrationForm.as_view()),
)
