"""
All drafting related Super Olympic logics and shits are kept here.
"""
from django.http import HttpResponse, HttpResponseRedirect
from data.models import  Player
from league.models import League
from team.models import  *
import json
from django.db.models import Q

def pic_player(request):
    return "joy bangla"

class MaxLimitException(Exception):
    pass


def get_my_team(legue_obj, user_obj):
    team = l.team_set.filter(user=user_obj)
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
                'save_queue_order' : save_queue
                }
            msg = func_map[func](data, request.user, l)
            result = 'success'
        except KeyError:
            result = 'error'
            in not msg: msg = 'Some player information is not sent! Cannot save the player.'
            print "Why the fuck: ", msg
        to_json = {'result': result, 'msg': msg}
        return HttpResponse(json.dumps(to_json), content_type='application/json')


def add_player(data, user):
    """
    Expected Json
    { 'player_id' : player_id,
      'position'  : position, # from position choices, `default` players default position
      'status'    : status,   # 'A' for active, 'B' for bench, 'W for waiting
      'rank'      : rank,  # 0 for adding to watch list, `default` 0
      'league_id' : league_id
      }
      add a player to your list, if 
         - user are authorised to make change in the team
         - user is not overflowing the league settings requirements
         - 
         #{u'player_id': u'ARIKK001', u'position': u'K', u'status': u'W', u'league_id': u'SKH0VX', u'rank': 0}
"""
    league_id = data['league_id']
    pid = data['player_id']
    status = data.get('status', 'W')
    rank = int(data.get('rank', '0'))
    
    player = Player.objects.get(pid=pid)
    position= data.get('position', player.position)
    l = League.objects.get(league_id=league_id)
    team = get_my_team(l, user)
            # check constraints
    s = l.settings
    if status!='W':
        num_players = team.fantasyplayer_set.filter(position=position).count()
        allowed_num = eval('s.count_%s_max' % position)
        if num_players>=allowed_num:
            msg = "Max allowed limmit(%d) for %s is reached" % ( num_players, QB )
            raise KeyError # should use custom exception
                
        f, isnew = FantasyPlayer.objects.get_or_create(player=player, team=team)
        f.position = position
        f.rank     = num_players+1
        if f.rank<=eval('s.count_%s_min' % ( position ) )+1:
            f.status = 'A'
        else:
            f.status = 'B'
    else: 
        num_players = team.fantasyplayer_set.filter(status='W').count()
        f, isnew = FantasyPlayer.objects.get_or_create(player=player, team=team)
        f.position = position
        f.rank     = num_players+1
        f.status = 'W'
        
        f.save()
        result = "success"
        msg = {'name': f.player.name, 'player_id' : pid, 'rank': f.rank, 'position':f.position }
        return msg


def save_queue_order(data, user):
    """
    { 'league_id': league_id, 'queue':queue }
    """
    # TODO: improve
    league_id = data['league_id']
    my_queue_order = data['queue']
    l = League.objects.get(league_id=league_id)
    team = get_my_team(l, user)
    my_queue = team.fantasyplayer_set.filter(status='W')
    for p in my_queue:
        i = my_queue_order.index(p.id)
        p.rank = i+1
    return ""


def delete_from_queue(data, user, l):
    removed_player_id = data['player_id']
    team = get_my_team(l,user)
    removed_buddy = team.fantasyplayer_set.filter(pid=data['removed_player'])
    players = team.fantasyplayer_set.filter(status='W').order_by('rank')
    rank = removed_buddy.rank
    for p in players[rank:]:
        p.rank=rank-1
        p.save()
    removed_buddy.delete()
    assert players[-1].rank==len(players)-1
    print players
    msg={"Deleted %s" % removed_buddy}


def autodrafting(data, user):
    pass


def populate_draft_page(league_id, user):
    l = League.objects.get(league_id=league_id)
    rteams = l.team_set.all()
    num_team = l.settings.number_of_teams
    teams = [ None ] * num_team # add Bots if `you` want
    for t in rteams:
        teams[t.draft_pick_number-1] = t
    # TODO
    players = Player.objects.filter()[:20]
    myteam  = l.team_set.filter(user=user)[0]
    print "MY TEAM NAME:", myteam.team_name
    res = {
        'teams' :  teams,
        'myteam': myteam,
        'myteam_watchlist': myteam.fantasyplayer_set.filter(rank=0),
        'myteam_players'  : myteam.fantasyplayer_set.filter(~Q(rank=0)),
        'players' : players,
        'league_id':league_id
    }
    return res

