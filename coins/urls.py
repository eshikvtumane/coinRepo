from django.conf.urls import patterns, include, url

from coins import views
urlpatterns = patterns('',
    # Examples:
    url(r'^$',views.index , name='home'),
    # url(r'^blog/', include('blog.urls')),


)
