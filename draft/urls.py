from django.conf.urls import patterns, url

from draft import views

urlpatterns = patterns('',
    url(r'^draftroom/(?P<draftroom_id>\w+)$', views.draftroom, name='draftroom'),
    url(r'^mockdraft/$', views.mockdraft, name='mockdraft'),
    url(r'^draft/(?P<draft_id>\d+)$', views.draft, name='draft'),
    url(r'^draft/$', views.draft, name='draft'),
)

