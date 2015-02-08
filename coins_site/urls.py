from django.conf.urls import patterns, include, url
from django.contrib import admin
#import django.contrib.staticfiles.views
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = patterns('',
    # Examples:
    url(r'^', include('main.urls')),
    url(r'^grappelli/', include('grappelli.urls')),
    url(r'^coins/',include('coins.urls')),
    # url(r'^blog/', include('blog.urls')),


    url(r'^user/', include('users.urls')),
    url(r'^news', include('news.urls')),

    url(r'shop/', include('shop.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^search/', include('haystack.urls')),
    (r'^messages/', include('django_messages.urls')),
)

#http://stackoverflow.com/questions/16196603/images-from-imagefield-in-django-dont-load-in-template
#https://docs.djangoproject.com/en/dev/howto/static-files/#deploying-static-files-in-a-nutshell
urlpatterns += staticfiles_urlpatterns()
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)