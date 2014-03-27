from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.template import Context, loader
from django.shortcuts import render, render_to_response
from data.models import Player, Team
from django.core import serializers

PLAYERS_FIELDS = ('name', 'team', 'position')
def index(request):
    try:
        s = int(request.GET.get('start', '0'))
    except:
        s = 0
    try:
        n = int(request.GET.get('num', '50'))
    except:
        n = 50
    n = min(n, 50)
    n = max(n, 0)
    s = max(s, 0)
    return HttpResponse(serializers.serialize("json",
        Player.objects.order_by('pk')[s:s+n],
        fields=PLAYERS_FIELDS, indent=2),
        content_type="application/json")

def info(request, player_id):
    return HttpResponse(serializers.serialize("json",
        [Player.objects.get(pk=player_id)], indent=2),
        content_type="application/json")
