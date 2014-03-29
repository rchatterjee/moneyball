"""
All drafting related Super Olympic logics and shits are kept here.
"""

from data.models import  Player
from league.models import League

def pic_player(request):
    return "joy bangla"

def populate_draft_page(league_id, user):
    l = League.objects.get(league_id=league_id)
    rteams = l.team_set.all()
    num_team = l.settings.number_of_teams
    teams = [ None ] * num_team # add Bots if `you` want
    for t in rteams:
        teams[t.draft_pick_number-1] = t
    # TODO
    players = Player.objects.filter(pk__lte=100)
    myteam  = l.team_set.filter(user=user)
    res = {
        'teams' :  teams,
        'myteam': myteam,
        'players' : players
    }
    return res

