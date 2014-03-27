from django.conf.urls import patterns, url

from league import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    url(r'^create/$', views.create, name='create'),
    url(r'^(?P<league_id>\d+)/$', views.league, name='index'),
    url(r'^(?P<league_id>\d+)/join/$', views.join, name='index'),
    url(r'^draftroom/', views.draftroom, name='draftroom'),
)

