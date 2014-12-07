from django.conf.urls import patterns, include, url
from views import CatalogView, SearchView, CoinsView,HomePage


urlpatterns = patterns('',
    url(r'^$', HomePage.as_view() , name='home'),
    url(r'search/',SearchView.as_view() , name='search-coin'),
    url(r'^catalog/$', CatalogView.as_view()),
    url(r'^catalog/(?P<country_id>[0-9]+)/$', CoinsView.as_view()),


)
