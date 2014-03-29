from django.conf.urls import patterns, url

from draft import views as dviews
from league import views as lviews
from draft.dodraft import *

urlpatterns = patterns('',
    url(r'^draftroom/(?P<draft_room_id>\w+)$', dviews.draft_room, name='draftroom'),
    url(r'^mockdraft/$', dviews.mock_draft, name='mockdraft'),
    url(r'^mockdraft/create/$', lviews.create, name='mockcreate'),
    url(r'^mockdraft/join/$', dviews.join_league, name='mockjoin'),
#    url(r'^mockdraft/(?P<league_id>\w+)/save/$', lviews.savesettings, name='savesettings'),
    url(r'^draft/(?P<draft_id>\w+)$', dviews.draft, name='draft'),


    # ajax urls
    url(r'addplayer/', add_player, name='addplayer')
)

