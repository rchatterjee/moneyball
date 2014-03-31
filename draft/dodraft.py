"""
All drafting related Super Olympic logics and shits are kept here.
"""
from django.http import HttpResponse, HttpResponseRedirect
from data.models import  Player
from league.models import League
from team.models import  *
import json
from django.db.models import Q
from collections import OrderedDict

def pic_player(request):
    return "joy bangla"

class MaxLimitException(Exception):
    pass

def get_my_team(league_obj, user_obj):
    team = league_obj.team_set.filter(user=user_obj)
    if team and team[0]: 
        team = team[0]
        return team
    else: 
        msg = "Sorry you dont have any team in this League."
        raise KeyError

def process_jquery_request(request):
    if request.is_ajax() and request.POST:
        result = ''
        msg=""
        try:
            data = json.loads(request.POST['data'])
            league_id = data['league_id']
            l = League.objects.get(league_id=league_id)
            func = data['func']
            func_map = {
                'add_player' : add_player,
                'save_queue_order' : save_queue_order,
                'get_player_info'  : get_player_info,
                'delete_from_queue'  : delete_from_queue
            }
            result = func_map[func](data, request.user, l)
            if 'result' not in result:
                result['result'] = 'success';
            print "Sending THis result:", result
        except KeyError:
            print request.POST
            print 'ERROR:', data
            result = 'error'
            if not msg: msg = 'Some player information is not sent! Cannot save the player.'
            print "Why the fuck: ", msg
        return HttpResponse(json.dumps(result), content_type='application/json')

# 1. check whether the player is available
# 2. check position wise max limit
# 3. check total team size is less than the max team size
# 4. already in list
def check_constraints(l, mt, p):
    for t in l.team_set.all():
        if t.fantasyplayer_set.filter(Q(player=p) & ~Q(status='Q')):
            msg = "Player is not Available!"
            return msg, False
    s = l.settings
    position_max = eval("s.count_%s_max" % p.position)
    my_player_at_this_position = mt.fantasyplayer_set.filter(Q(position=p.position) & ~Q(status='Q'))
    if len(t.fantasyplayer_set.all())>=s.size:
        msg = "No space left in your team!"
        return msg, False
    if len(my_player_at_this_position)>=position_max:
        if not t.fantasyplayer_set.filter(position="FLEX"):
            msg = "Already selected %d '%s' players" % (len(my_player_at_this_position), p.position)
        else:
            msg = "Can be added to Flex!"
        return msg, False
    return len(my_player_at_this_position), True



def add_player(data, user, l):
    pid = data['player_id']
    status = data.get('status', 'Q')
    player = Player.objects.get(pid=pid)
    position=player.position
    team = get_my_team(l, user)
    # check constraints
    print 'Start1:', data
    s = l.settings
    if status != 'Q':
        msg, okay = check_constraints(l, team, player)
        print msg, okay
        if not okay:
            return {'result': 'error', 'msg': msg}
        f, isnew = FantasyPlayer.objects.get_or_create(player=player, team=team)
        f.position = position
        f.rank     = msg+1
        if f.rank <= eval('s.count_%s_min' % position):
            f.status = 'A'
        else:
            f.status = 'B'
        f.save()
    else:
        num_players = team.fantasyplayer_set.filter(status='Q').count()
        f, isnew = FantasyPlayer.objects.get_or_create(player=player, team=team)
        if not isnew:
            return {'result': 'error', 'msg': "Already in Queue or Selected"}
        f.position = position
        f.rank     = num_players+1
        f.status = 'Q'
        f.save()

    msg = {'name': f.player.name,
           'player_id': pid,
           'rank': f.rank,
           'position': f.position,
           'status': f.status
    }
    result = {'result': 'success', 'msg': msg}
    return result


def save_queue_order(data, user):
    """
    { 'league_id': league_id, 'queue':queue }
    """
    # TODO: improve
    league_id = data['league_id']
    my_queue_order = data['queue']
    l = League.objects.get(league_id=league_id)
    team = get_my_team(l, user)
    my_queue = team.fantasyplayer_set.filter(status='Q')
    for p in my_queue:
        i = my_queue_order.index(p.id)
        p.rank = i+1
    return ""


def get_player_info(data, user, league):
    print data
    player = Player.objects.get(pid=data['player_id'])
    msg = {
        'position': player.position,
        'name'    : player.name,
        'team'    : player.team.name,
        'rank'    : 1,
        'more'    : "This player is the only player in the world you should choose next. Otherwise the world will fall!!"
    }
    return {'result':'success', 'msg': msg};


def delete_from_queue(data, user, l):
    team = get_my_team(l,user)
    print team
    removed_buddy = team.fantasyplayer_set.filter(player__pid=data['player_id'])[0]

    players = [ x for x in team.fantasyplayer_set.filter(status='Q').order_by('rank')]
    print '\n'.join([str(x) for x in players])
    print "Removing:", removed_buddy
    rank = removed_buddy.rank
    if len(players)>rank+1:
        print players[rank:]
        for i,p in enumerate(players[rank:]):
            print i, p, p.rank, rank
            p.rank = rank-1+i+1
            p.save()
    removed_buddy.delete()
    msg= "Deleted %s" % removed_buddy
    return {'result': 'success', 'msg': msg}


def auto_drafting(data, user):
    pass


def populate_draft_page(league_id, user):
    l = League.objects.get(league_id=league_id)
    s = l.settings
    rteams = l.team_set.all()
    num_team = s.number_of_teams
    teams = [ None ] * num_team # add Bots if `you` want
    for t in rteams:
        teams[t.draft_pick_number-1] = t
    # TODO
    players = Player.objects.filter()[:20]
    myteam  = l.team_set.filter(user=user)[0]

    allowed_player_types = ['QB', 'RB', 'WR', 'TE', 'FLEX', 'K', 'BN']
    roster_settings = {'size' : s.size, 'starters':s.starters, 'benched': s.benched}
    curr_team = OrderedDict()
    myplayer_set = myteam.fantasyplayer_set.all()

    bench_count = 0
    for a in allowed_player_types:
        if a == 'BN':
            this_type_player = myplayer_set.filter(status='B')
            min_count = bench_count = len(this_type_player)
        else:
            this_type_player = myplayer_set.filter(Q(position=a) & ~Q(status='Q')).order_by('rank')
            min_count = eval("s.count_%s_min" % a)

        for n in range(min_count):
            if n < len(this_type_player):
                curr_team['%s%d'%(a, n+1)] = this_type_player[n].player.name
            else:
                curr_team['%s%d'%(a, n+1)] = '[EMPTY]'

    print "MY TEAM NAME:", myteam.team_name
    res = {
        'teams' :  teams,
        'myteam': myteam,
        'myteam_queue': myteam.fantasyplayer_set.filter(status='Q'),
        'myteam_players'  : myteam.fantasyplayer_set.filter(Q(status='A')| Q(status='B')),
        'players' : players,
        'league_id':league_id,
        'roster_settings' : roster_settings,
        'current_team' : curr_team,
        'bench_count'  : bench_count
    }
    return res

