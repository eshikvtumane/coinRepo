from django.conf.urls import patterns, include, url
from views import CatalogView, SearchView, CoinsView, CoinSelectView


from coins import views

urlpatterns = patterns('',
    url(r'search/',views.SearchView.as_view() , name='search-coin'),
    #url(r'country_ajax/',views.ajax,name='country-ajax'),
    url(r'^catalog/$', CatalogView.as_view()),
    url(r'^catalog/(?P<country_id>[0-9]+)/$', CoinsView.as_view()),
    url(r'^catalog/(?P<country_id>[0-9]+)/(?P<coin_id>[0-9]+)/$', CoinSelectView.as_view()),
   



)
