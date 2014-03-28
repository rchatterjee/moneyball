from django.conf.urls import patterns, url

from draft import views as dviews
from league import views as lviews

urlpatterns = patterns('',
    url(r'^draftroom/(?P<draftroom_id>\w+)$', dviews.draftroom, name='draftroom'),
    url(r'^mockdraft/$', dviews.mockdraft, name='mockdraft'),
    url(r'^mockdraft/create/$', lviews.create, name='mockcreate'),
    url(r'^mockdraft/join/$', dviews.joinleague, name='mockjoin'),
    url(r'^draft/(?P<draft_id>\d+)$', dviews.draft, name='draft'),
    url(r'^draft/$', dviews.draft, name='draft'),
)

