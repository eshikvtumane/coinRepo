from django.conf.urls import patterns, include, url
from views import HomeView

urlpatterns = patterns('',
    # Examples:
    url(r'^$', HomeView.as_view()),
)