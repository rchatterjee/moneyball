from django.shortcuts import render
from django.http import HttpResponse
from team.models import Team
from league.models import *
from league.views import generate_random_id
from django.contrib.auth.decorators import login_required
import re
from ffball.settings import errors

def index(request):
    context = { 'teams': [str(x) for  x in Team.objects.filter(user=request.user)]}
    return HttpResponse("<h1>Teams:<h1>%s<hr/>%s" % ( '<br/><hr/>'.join(context['teams']) ))


def get_draft_pick_number(l):
    teams_dpn = [t.draft_pick_number for t in l.team_set.all()]
    teams_dpn.sort()
    for i in range(1, l.settings.number_of_teams+1):
        if i>len(teams_dpn) or i<teams_dpn[i]:
            return i    


@login_required
def create_team(request, is_commissioner=0, league_id = ''):
    global errors
    league_id = request.POST.get('leagueId', league_id)
    team_name = request.POST.get('teamName', '')
    password  = request.POST.get('entryKey', '')
    errors = []
    if not ( league_id and team_name):
        errors.append("<br/> League id and/or team_name is none!")
        return None
    
    l = League.objects.get(league_id=league_id)
    teams = l.team_set.all()    
    user = request.user

    if (not is_commissioner) and (l.password) and (password != l.password):
        errors.append("<br/> - Password did not match!")
    if l.settings.number_of_teams <= len(teams):
        errors.append("<br/> - league is already full!")
        print errors, l.settings.number_of_teams, teams
    if user in [t.user for t in teams]:
        errors.append("<br/> - you (%s) already have a team in this league! click inside the league to know about it." % request.user)
        print errors, user, [t.user for t in teams]
    if errors:
        return None

    vendor_team_id = generate_random_id(4)
    vendor_user_id = 'xxyyzz'
    waiver_priority = 1
    division = ''
    draft_pick_number = get_draft_pick_number(l);
    t = Team(league=l,
             user=user,
             vendor_team_id=vendor_team_id,
             vendor_user_id=vendor_user_id,
             team_name=team_name,
             waiver_priority=waiver_priority,
             division=division,
             is_commissioner=is_commissioner,
             draft_pick_number=draft_pick_number)
    return t


def delete(request):
    global errors
    t_id = request.POST.get('id', 0)
    team = request.user.Teams.all(id=t_id)
    if request.user.is_authenticated() and team:
        team.delete()
        h = HttpResponse()
        errors = "<b>Successfully deleted the team %s" % team.name
        context = []
        return render(request, h, {'errors':errors})
    else:
        return HttpResponse("<error>Sorry Dude! Tumse na ho payega!!.<error>")
    

def edit(request):
    pass


def desc(request, _id):
    t = Team.objects.filter(user=request.user, id=_id)
    description = str(vars(t))
    if t:
        context = {'team': description}
        return HttpResponse(context['description'])
    return HttpResponse("OMG! this is you %s" % str(request.user))


redirect_map = { '' : index,
            'create' : create_team,
             'delete' : delete,
             'edit'   : edit
}

def redirect(request, action):
    try:
        if not request.user.is_authenticated():
            raise KeyError;
    except KeyError:
        return HttpResponse("<error>Sorry! You don't look like an authorised user for this action.<error>")
    try:
        action = action.strip('/')
        return redirect_map[action](request)
    except KeyError:
        m = re.match(r'(?P<id>\d+)', action)
        if m:
            id = int(m.group('id'))
            return desc(request, id)
    return HttpResponse("<error>Page Not Found.<error>")


