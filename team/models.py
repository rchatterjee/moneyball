from django.db import models as m
from league.models import League
from django.contrib.auth.models import User
from data.models import  Player

class Team(m.Model):
    league         = m.ForeignKey(League)
    user           = m.ForeignKey(User)
    vendor_team_id = m.CharField(max_length=30, blank=True)
    vendor_user_id = m.CharField(max_length=40, blank=False)
    team_name      = m.CharField(max_length=100, blank=False)
    waiver_priority= m.IntegerField(null=True)
    division       = m.CharField(max_length=10, blank=True, null=True)
    is_commisionar = m.BooleanField(default=False)
    draft_pick_number = m.IntegerField(default=-1, null=True)
    image_name = m.CharField(max_length=15, blank=True, null=True, default='0.jpg')

    #draft time updates
    watch_list = m.ManyToManyField(Player, related_name='team_watchlist', null=True, blank=True, default = None)

    def __str__(self):
        return "(%d)%s - %s" % ( self.pk, self.team_name, self.league )


FANTASY_PLAYER_POSITION_CHOICES = (
    ('QB', 'Quarter Back'),
    ('RB', 'Running Back'),
    ('W', 'Wide Receiver'),
    ('TE', 'Tide End'),
    ('K', 'Kicker'),
    ('DEF', 'Defence'),
    ('FLEX', 'Flex')
)
FANTASY_PLAYER_STATUS_CHOICES = (
    ('A', 'Active'),
    ('B', 'Bench' )
)
class FantasyPlayer(m.Model):
    player = m.ForeignKey(Player)
    position = m.CharField(max_length=4, choices=FANTASY_PLAYER_POSITION_CHOICES, default='FLEX', null=True)
    team = m.ForeignKey(Team)
    status = m.CharField(max_length=1, choices=FANTASY_PLAYER_STATUS_CHOICES)

    def __str__(self):
        return "%s (%s)" % ( self.player.name )
