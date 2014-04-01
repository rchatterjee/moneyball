from django.db import models as m
from league.models import League
from django.contrib.auth.models import User
from data.models import  Player
from django.db.models import Q
import random, sys

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
    auto_draft     = m.BooleanField(default=False)
    image_name = m.CharField(max_length=15, blank=True, null=True, default='0.jpg')
    #draft time updates


    def add_player_to_team(self, player=None, pid=None):
        if not player and not pid: return False;
        if not player: player = Player.objects.get(pid=pid)
        f, isnew = FantasyPlayer.objects.get_or_create(player=player, team=self)
        f.position = player.position #FLEX?
        f.rank     = self.fantasyplayer_set.filter(Q(position=player.position) & ~Q(status='Q')).count()+1
        if f.rank <= eval('s.count_%s_min' % f.position):
            f.status = 'A'
        else:  # TODO add flex
            f.status = 'B'
        f.save()
        return True

    def add_player_to_Q(self, player=None, pid=None):
        f, isnew = FantasyPlayer.objects.get_or_create(player=player, team=self)
        if not isnew:
            return None
        f.position = player.position   #FLEX?
        f.rank     = self.fantasyplayer_set.filter(status='Q').count()+1
        f.status = 'Q'
        f.save()
        return f

    def pick_best_available_player(self, position, count=1):
        P = Player.objects.filter(position=position)
        ret = []
        for i in range(count):
            ret.append(random.choice(P))
        return ret

    def pop_first_player_inQ(self):
        Q= self.fantasyplayer_set.filter(status='Q').order_by('rank')
        if Q: return Q[0]
        else:
            s = self.league.settings
            for pos in ['QB', 'RB', 'WR', 'TE', 'K', 'BN']:
                for p in self.pick_best_available_player(pos, eval("s.count_%s_min" % pos)+1):
                    self.add_player_to_Q(p)
            return self.pop_first_player_inQ()

    def auto_draft_player(self):
        print __name__, sys._getframe().f_code.co_name
        if not self.auto_draft: return False;
        if not self.add_player_to_team(self.pop_first_player_inQ()):      # try once more
            self.add_player_to_team(self.pop_first_player_inQ())
        return True;

    def is_full(self):
        return self.fantasyplayer_set.filter(~Q(status='Q')).count()>=self.league.settings.size

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
