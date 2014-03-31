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
    is_commissioner= m.BooleanField(default=False)
    draft_pick_number = m.IntegerField(default=-1, null=True)
    image_name = m.CharField(max_length=15, blank=True, null=True, default='0.jpg')
    #draft time updates
    # CONVENTION:
    # watch_list is FantasyPlayers with non-zero rank
    # FantasyPlayers with zero rank are already in my team

    def __str__(self):
        if self.pk:
            return "(%d)%s - %s" % ( self.pk, self.team_name, self.league )
        else:
            return "(0)%s - %s" % ( self.team_name, self.league )


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
    ('B', 'Bench' ),
    ('Q', 'Queue')
)

class FantasyPlayer(m.Model):
    player   = m.ForeignKey(Player)
    position = m.CharField(max_length=4, choices=FANTASY_PLAYER_POSITION_CHOICES, default='FLEX', null=True)
    team     = m.ForeignKey(Team)
    status   = m.CharField(max_length=1, choices=FANTASY_PLAYER_STATUS_CHOICES)
    rank     = m.IntegerField(default=0, null=True) # only if he is in watchlist

    def __str__(self):
        return "Player: {name: %s, team: %s, position: %s, rank: %d}" % ( self.player.name, self.team.team_name, self.position, self.rank )



TRANSACTION_ACTION_CHOICES = (
    ('ADD', 'Add Player'),
    ('DEL', 'Delete Player'),
    ('TRD', 'Trade Player'),

)
# TODO
class Transaction(m.Model):
    created_at = m.DateTimeField(auto_now_add=True)
    action     = m.CharField(max_length=4, choices=TRANSACTION_ACTION_CHOICES)
    player1    = m.ForeignKey(FantasyPlayer, null=True, blank=True)
    player1    = m.ForeignKey(FantasyPlayer, null=True, blank=True)

    def __str__(self):
        return "%s (%s)" % ( self.player.name )
