from django.db import models as m
from league.models import League
from django.contrib.auth.models import User

class Team(m.Model):
    league         = m.ForeignKey(League)
    user           = m.ForeignKey(User)
    vendor_team_id = m.CharField(max_length=30, blank=True)
    vendor_user_id = m.CharField(max_length=40, blank=False)
    team_name      = m.CharField(max_length=100, blank=False)
    waiver_priority= m.IntegerField(null=True)
    division       = m.CharField(max_length=10,null=True)
    is_commisionar = m.BooleanField(default=False)

    def __str__(self):
        return "%s - %s" % ( self.team_name, self.league )
