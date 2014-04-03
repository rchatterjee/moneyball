from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.template import Context, loader
from django.shortcuts import render, render_to_response
from data.models import Player, Team, AggStat
from team.models import FantasyPlayer
from django.core import serializers
from django.db.models import Q
import json, pprint

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
    'qb': Q(player__position = 'QB'),
    'rb': Q(player__position = 'RB'),
    'wr': Q(player__position = 'WR'),
    'te': Q(player__position = 'TE'),
    'k': Q(player__position = 'K'),
}

ORDER_BY_MAP = {
    'name': 'player__name',
    'position':'player__position',
    'team':'player__team',
}

def order_size(request):
    f = request.GET.get('type', 'all')
    id = request.GET.get('league_id', '')
    if not FILTER_MAP.has_key(f):
        f = 'all'
    existing = FantasyPlayer.objects \
            .filter(team__league__league_id = id) \
            .values_list('player__pid', flat=True)
    size = AggStat.objects.exclude(player__pid__in = existing) \
            .filter(FILTER_MAP[f]).count()
    return HttpResponse(json.dumps(size),
        content_type="application/json")

STATS_FIELD = [
    'player__pid',
    'player__team',
    'player__position',
    'player__name' ]

def stats_serialize(a, fields):
    l = []
    for v in a.values(*(STATS_FIELD + fields)):
        l.append({'pk': '',
                'model': 'data.aggstat',
                'fields': v})
    return HttpResponse(json.dumps(l, indent=2),
            content_type="application/json")

def order(request):
    f = request.GET.get('type', 'all')
    o = request.GET.get('sort', 'player__name')
    s = int(request.GET.get('start', '0'))
    l = int(request.GET.get('length', '20'))
    id = request.GET.get('league_id', '');
    fields = request.GET.get('fields', '')
    fields = fields.split(',')
    if not FILTER_MAP.has_key(f):
        f = 'all'
    s = max(0, s)
    l = max(0, l); l = min(50, l)

    existing = FantasyPlayer.objects \
            .filter(team__league__league_id = id) \
            .values_list('player__pid', flat=True)
    a = AggStat.objects.exclude(player__pid__in = existing) \
            .select_related('player').filter(FILTER_MAP[f]) \
            .order_by(o)[s:s+l]
    return stats_serialize(a, fields)

SEARCH_FIELDS = ['player__name', 'player__pid']
def search_serialize(a):
    l = []
    for v in a.values(*SEARCH_FIELDS):
        l.append({'pk': v['player__pid'],
                'model': 'data.aggstat',
                'fields': v})
    return HttpResponse(json.dumps(l, indent=2),
            content_type="application/json")

def search(request):
    q = request.GET.get('q', '')
    id = request.GET.get('league_id', '');
    print (q, id)
    existing = FantasyPlayer.objects \
            .filter(team__league__league_id = id) \
            .values_list('player__pid', flat=True)
    a = AggStat.objects.exclude(player__pid__in = existing) \
            .select_related('player') \
            .filter(player__name__contains=q) \
            .order_by('player__name')[:10]
    return search_serialize(a)

def info(request, player_id):
    return HttpResponse(serializers.serialize("json",
        [Player.objects.get(pk=player_id)], indent=2),
        content_type="application/json")
