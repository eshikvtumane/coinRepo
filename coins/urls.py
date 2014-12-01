from django.conf.urls import patterns, include, url

from coins import views
urlpatterns = patterns('',
    # Examples:
    url(r'^$',views.index , name='home'),
    url(r'search/',views.SearchView.as_view() , name='search-coin'),
    url(r'country_ajax/',views.ajax,name='country-ajax')
    # url(r'^blog/', include('blog.urls')),


)
