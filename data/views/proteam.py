from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.template import Context, loader
from django.shortcuts import render, render_to_response
from data.models import Player, Team
from django.core import serializers

TEAMS_FIELDS = ('name', 'home')
def index(request):
    return HttpResponse(serializers.serialize("json",
        Team.objects.all(), fields=TEAMS_FIELDS, indent=2),
        content_type="application/json")

def info(request, team_id):
    return HttpResponse(serializers.serialize("json",
        [Team.objects.get(pk=team_id)], indent=2),
        content_type="application/json")

PLAYER_FIELDS = ('name', 'position')
def players(request, team_id):
    return HttpResponse(serializers.serialize("json",
        Player.objects.filter(team_id=team_id),
        fields=PLAYER_FIELDS, indent=2),
        content_type="application/json")
