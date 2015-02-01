from django.conf.urls import patterns, include, url
from views import SellerSettings, CreateLot, SearchCoinsView, DeliveryAddressView

from coins import views
urlpatterns = patterns('',
    # Examples:
    #url(r'^$',views.index , name='home'),
    #url(r'search/',views.SearchView.as_view() , name='search-coin'),
    url(r'settings/', SellerSettings.as_view()),
    url(r'create_buy/', CreateLot.as_view()),
    # delivery address
    url(r'^delivery_address/$', DeliveryAddressView.as_view()),

    # ajax
    url(r'coin_search/', SearchCoinsView.as_view()),

)