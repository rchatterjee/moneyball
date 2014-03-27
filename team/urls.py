__author__ = 'rchat'
from django.conf.urls import patterns, include, url
import team.views
urlpatterns = patterns('',
    url(r'^team/(\w*)', team.views.redirect, name='team'),
)
