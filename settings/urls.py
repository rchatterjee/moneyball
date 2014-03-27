from django.conf.urls import patterns, include, url
from settings.views import *
from django.contrib import admin
#import team
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^blog/', include('blog.urls')),
    url(r'^settings/', index, name='index'),
)
