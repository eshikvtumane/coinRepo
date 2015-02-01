from django.conf.urls import patterns, include, url
from views import CatalogView, SearchView, CoinsView, CoinSelectView


from coins import views

urlpatterns = patterns('',
    #url(r'country_ajax/',views.ajax,name='country-ajax'),
    url(r'^catalog/$', CatalogView.as_view()),
    url(r'^catalog/(?P<country_id>\d+)/$', CoinsView.as_view()),
    url(r'^catalog/(?P<country_id>\d+)/(?P<coin_id>\d+)/$', CoinSelectView.as_view()),
    url(r'^catalog/search/',views.SearchView.as_view() , name='search-coin')
)
