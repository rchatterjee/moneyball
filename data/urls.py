from django.conf.urls import patterns, url

from data.views import proteam as tviews
from data.views import proplayer as pviews

urlpatterns = patterns('',
    url(r'^proteam/$', tviews.index, name='proteam.index'),
    url(r'^proteam/(?P<team_id>\d+)$', tviews.info, name='proteam.info'),
    url(r'^proteam/(?P<team_id>\d+)/players$',
        tviews.players, name='proteam.players'),
    url(r'^proplayer/$', pviews.index, name='index'),
    url(r'^proplayer/(?P<player_id>\d+)/$', pviews.info, name='index'),
)
