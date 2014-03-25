#!/usr/bin/python
"""
One who is playing the fantasy football and using our app is 'User'
Who is playing American Foot ball is a 'Player'
"""

from __future__ import unicode_literals
from django.db import models as m
from league_settings_model import League_Settings
import historical_data_models
#from check_constraints import Check, CheckConstraintMetaClass
from django.contrib.auth.models import User

PLAYER_STATUS_COICES = (
    ('A', 'active'),
    ('B', 'benched')
)

TRANSACTION_TYPE_CHOICES = (
    ('AD', 'add-drop'),
    ('A',  'add'),
    ('D', 'drop'),
    ('T', 'trade')
)

TRANSACTION_STATUS_CHOICES = (
    ('P', 'pending'),
    ('A', 'approved'),
    ('C', 'cancelled'),
    ('F', 'free-agent-pickup'),
    ('W', 'waiver-pickup')
)

class Vendor(m.Model):
    name    = m.CharField(max_length=40, blank=False)
    website = m.CharField(max_length=250, blank=False)

class League(m.Model):
    name   = m.CharField(max_length=100, blank=False)
    vendor = m.ForeignKey(Vendor)
    league_id = m.CharField(max_length=50, blank=True)
    # settings 
    settings = m.ForeignKey(League_Settings)

class Team(m.Model):
    league         = m.ForeignKey(League)
    user           = m.ForeignKey(User) 
    vendor_team_id = m.CharField(max_length=30, blank=True)
    user_id        = m.CharField(max_length=40, blank=False)
    team_name      = m.CharField(max_length=100, blank=False)
    waiver_priority= m.IntegerField(null=True)
    division       = m.CharField(max_length=10,null=True)

class Player(m.Model):
    roster_info = m.OneToOneField(historical_data_models.Player)
    status      = m.CharField(max_length=1, choices=PLAYER_STATUS_COICES,
                                  default='A')
    team = m.ManyToManyField(Team)
    
class Transaction(m.Model):
    T_type = m.CharField(max_length=2, choices=TRANSACTION_TYPE_CHOICES,
                         default='A')

    team1   = m.ManyToManyField(Team, related_name="Team1")
    player1 = m.ForeignKey(Player, related_name="Player1")
    team2   = m.ManyToManyField(Team, null=True, blank=True, default = None,
                                related_name="Team2" ) # NULL if Add/Drop/Add-drop only 
    player2 = m.ForeignKey(Player, null=True, blank=True, default = None, 
                           related_name="Player2") # NUll if Add/Drop
    status  = m.CharField(max_length=1, choices=TRANSACTION_STATUS_CHOICES,
                          default='A')
    timestamp = m.DateTimeField('Transaction Time')
    
    # team1 and team2 should not be equal
    # player1 and player2 should not be equal

    def save(self):
        if self.player1 == self.player2:
            raise(Exception, "Same player cannot be added and dropped.") 
        elif self.team1 == self.team2:
            raise(Exception, "Same team cannot trade between themselves")
        else:
            super(Transaction, self).save()
    # class Meta:
    #     constraints = (
    #         ("check_player1player2", Check(player1__neq = 'player2')),
    #         ("check_team1team2",     Check(team1__neq   = 'team2'))
    #         )
                
