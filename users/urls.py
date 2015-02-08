#-*- coding:utf-8 -*-
from django.conf.urls import patterns, include, url
from django.contrib import admin
from users import *
from . import views
urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'coins_site.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^authentication/$', views.UserAuth.as_view()),
    url(r'^register/$', views.UserRegistration.as_view()),
    url(r'^logout/$', views.UserLogout.as_view()),
    url(r'^info/$', views.UserInfo.as_view()),
    url(r'^info/reset_password/$', views.PasswordReset.as_view()),


    #for collections
    url(r'^collections/$', views.UserCountryView.as_view()),
    url(r'^ajax/add/country/$', views.UserCountryView.as_view()),
      # добавление серий
    url(r'collections/(?P<country_id>[0-9]+)/$', views.UserSeriesView.as_view()),
    url(r'ajax/add/series/$', views.UserSeriesView.as_view()),

        # добавление монет
    url(r'collections/(?P<country_id>[0-9]+)/(?P<series_id>[0-9]+)/$', views.UserCoinsView.as_view()),
    url(r'ajax/add/coins/$', views.UserCoinsView.as_view()),

    # добавление разновидностей монет
    url(r'collections/(?P<country_id>[0-9]+)/(?P<series_id>[0-9]+)/(?P<coin_id>[0-9]+)/$', views.UserCoinInfoView.as_view()),

    url(r'series/delete/$', views.SeriesDeleteView.as_view()),
    url(r'country/delete/$', views.CountryDeleteView.as_view()),
    url(r'coin/delete/$', views.CoinDeleteView.as_view()),

    url(r'coininfo/change/$', views.CoinInfoChangeView.as_view()),


    # import in XLS
    url(r'import/$', views.GenerateXlsView.as_view()),
)
