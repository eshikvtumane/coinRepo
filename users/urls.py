#-*- coding:utf-8 -*-
from django.conf.urls import patterns, include, url
from django.contrib import admin
from users import *
from users.views import UserRegistration, UserAuth, UserLogout, UserInfo, UserCountryView, UserSeriesView, UserCoinsView, UserCoinInfoView, SeriesDeleteView, CountryDeleteView, CoinDeleteView,CoinInfoChangeView, GenerateXlsView

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'coins_site.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^authentication/$', UserAuth.as_view()),
    url(r'^register/$', UserRegistration.as_view()),
    url(r'^logout/$', UserLogout.as_view()),
    url(r'^info/$', UserInfo.as_view()),

    #for collections
    url(r'^collections/$', UserCountryView.as_view()),
    url(r'^ajax/add/country/$', UserCountryView.as_view()),
      # добавление серий
    url(r'collections/(?P<country_id>[0-9]+)/$', UserSeriesView.as_view()),
    url(r'ajax/add/series/$', UserSeriesView.as_view()),

        # добавление монет
    url(r'collections/(?P<country_id>[0-9]+)/(?P<series_id>[0-9]+)/$', UserCoinsView.as_view()),
    url(r'ajax/add/coins/$', UserCoinsView.as_view()),

    # добавление разновидностей монет
    url(r'collections/(?P<country_id>[0-9]+)/(?P<series_id>[0-9]+)/(?P<coin_id>[0-9]+)/$', UserCoinInfoView.as_view()),

    url(r'series/delete/$', SeriesDeleteView.as_view()),
    url(r'country/delete/$', CountryDeleteView.as_view()),
    url(r'coin/delete/$', CoinDeleteView.as_view()),

    url(r'coininfo/change/$', CoinInfoChangeView.as_view()),


    # import in XLS
    url(r'import/$', GenerateXlsView.as_view()),
)
