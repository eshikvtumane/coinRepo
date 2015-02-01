from django.conf.urls import patterns, include, url
from views import CatalogView, SearchView, CoinsView, CoinSelectView, WishListView, WLView
from users.views import UserCoinInfoView

from coins import views
urlpatterns = patterns('',
    # Examples:
    #url(r'^$',views.index , name='home'),
    url(r'catalog/search/',views.SearchView.as_view() , name='search-coin'),
    #url(r'country_ajax/',views.ajax,name='country-ajax'),
    url(r'^catalog/$', CatalogView.as_view()),
    url(r'^catalog/city/(?P<country_id>[0-9]+)/$', CoinsView.as_view()),
    url(r'^catalog/city/(?P<country_id>[0-9]+)/(?P<coin_id>[0-9]+)/$', CoinSelectView.as_view()),
    url(r'^catalog/city/(?P<country_id>[0-9]+)/(?P<series_id>[0-9]+)/(?P<coin_id>[0-9]+)/$', CoinSelectView.as_view()),
    # wish list
    url(r'^wish_list/(?P<username>[A-Za-z0-9]+)/$', WLView.as_view()),

    # ajax
    url(r'^add_wish_list/$', WishListView.as_view()),
   # redirect to users catalogue
    url(r'collections/(?P<country_id>[0-9]+)/(?P<series_id>[0-9]+)/(?P<coin_id>[0-9]+)/$', UserCoinInfoView.as_view()),

    # url(r'^blog/', include('blog.urls')),

)

