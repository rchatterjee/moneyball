from django.db import models as m
import ffball.fantasy_models as ffmodel
from django.contrib.auth.models import User


class Team(m.Model):
    league         = m.ForeignKey(ffmodel.League)
    user           = m.ForeignKey(User)
    vendor_team_id = m.CharField(max_length=30, blank=True)
    user_id        = m.CharField(max_length=40, blank=False)
    team_name      = m.CharField(max_length=100, blank=False)
    waiver_priority= m.IntegerField(null=True)
    division       = m.CharField(max_length=10,null=True)
