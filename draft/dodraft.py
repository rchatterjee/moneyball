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


def add_player(request):
    """
    Expected Json
    { 'player_id' : player_id,
      'position'  : position, # from position choices, `default` players default position
      'status'    : status,   # 'A' for active, 'B' for bench
      'rank'      : rank,  # 0 for adding to watch list, `default` 0
    """

    if request.is_ajax() and request.POST:
        result = "error"
        msg=""
        try:
            #{u'player_id': u'ARIKK001', u'position': u'K', u'status': u'W', u'league_id': u'SKH0VX', u'rank': 0}
            data = json.loads(request.POST['data'])
            league_id = data['league_id']
            pid = data['player_id']
            status = data['status']
            rank = int(data.get('rank', '0'))
            player = Player.objects.get(pid=pid)
            print "Player:", player
            position= data.get('position', player.position)
            l = League.objects.get(league_id=league_id)
            team = l.team_set.filter(user=request.user)
            if team: team = team[0]
            f, isnew = FantasyPlayer.objects.get_or_create(player=player, team=team)
            f.position = position
            f.rank     = rank
            f.status   = status
            f.save()
            result = "success"
            msg = {'name': f.player.name }
        except KeyError:
            msg = 'Some player information is not sent! Cannot save the player.'
            print "Why the fuck", msg
        except:
            print "You suck"
        to_json = {'result': result, 'msg': msg}
        return HttpResponse(json.dumps(to_json), content_type='application/json')


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

