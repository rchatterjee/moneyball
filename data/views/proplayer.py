from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.template import Context, loader
from django.shortcuts import render, render_to_response
from data.models import Player, Team
from django.core import serializers
from django.db.models import Q
import json

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

FILTER_MAP = {
    'all': Q(),
    'qb': Q(position = 'QB'),
    'rb': Q(position = 'RB'),
    'wr': Q(position = 'WR'),
    'te': Q(position = 'TE'),
    'k': Q(position = 'K'),
}

ORDER_BY_MAP = {
    'name': 'name',
    'position':'position',
    'team':'team',
}

def order_size(request):
    f = request.GET.get('type', 'all')
    if not FILTER_MAP.has_key(f):
        f = 'all'
    size = Player.objects.filter(FILTER_MAP[f]).count()
    return HttpResponse(json.dumps(size),
        content_type="application/json")

def order(request):
    f = request.GET.get('type', 'all')
    o = request.GET.get('sort', 'name')
    s = int(request.GET.get('start', '0'))
    l = int(request.GET.get('length', '20'))
    if not FILTER_MAP.has_key(f):
        f = 'all'
    if not ORDER_BY_MAP.has_key(o):
        o = 'name'
    s = max(0, s)
    l = max(0, l); l = min(50, l)
    return HttpResponse(serializers.serialize("json",
        Player.objects.filter(FILTER_MAP[f]) \
            .order_by(ORDER_BY_MAP[o])[s:s+l], indent=2),
            content_type="application/json")

def info(request, player_id):
    return HttpResponse(serializers.serialize("json",
        [Player.objects.get(pk=player_id)], indent=2),
        content_type="application/json")
