from django.shortcuts import render
from django.http import HttpResponse
import re
from django.contrib.auth.models import User
from team.models import Team
from league.models import *
from league.views import generate_random_id


def index(request):
    context = { 'teams': Team.objects.filter(user=request.user) }
    return HttpResponse("<h1>Teams:<h1>%s" % context['teams'])
    #return render(request, 'views.html', context);


def create(request):
    user_id = request.user.id
    error = ''
    league_id         = request.POST.get('league_id', None)
    if not league_id or not league_id.isdigit():
        error = "%s\nLeagueId is not in correct format or not present." % error
    user          = request.user
    vendor_team_id = request.POST.get('vender_team_id', None)
    vendor_user_id = request.POST.get('vendor_user_id', None)
    team_name      = request.POST.get('team_name', '')
    waiver_priority= request.POST.get('waiver_priority', None)
    division       = request.POST.get('division', None)
    if not error:
        T = Team.create(league_id, user, vendor_team_id, vendor_user_id, team_name,
                        waiver_priority, division)
        T.save()
        h = HttpResponse("<b>Successfully created the team %s" % team_name)
        context = []
        return render(request, h, context)
    else:
        return HttpResponse("<error>ERRORS! %s.<error>" % error)

def delete(request):
    t_id = request.POST.get('id', 0)
    team = request.user.Teams.all(id=t_id)
    if request.user.is_authenticated() and team:
        team.delete()
        h = HttpResponse("<b>Successfully deleted the team %s" % team_name)
        context = []
        return render(request, h, context)
    else:
        return HttpResponse("<error>Sorry Dude! Tumse na ho payega!!.<error>")
    

def edit(request):
    pass


def desc(request, _id):
    t = Team.objects.filter(user=request.user, id=_id)
    if t:
        context = {'team': t}
        return HttpResponse(context['team'])
    return HttpResponse("OMG! this is you %s" % str(request.user))


redirect_map = { '' : index,
            'create' : create,
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



def create_team(request, is_commisionar=0, league_id = ''):
    league_id = request.POST.get('leagueId', league_id)
    team_name = request.POST.get('teamName', '')
    password  = request.POST.get('entryKey', '')
    error = ''
    if not ( league_id and team_name):
        error = "<br/> League id and/or team_name is none!"
        print error, " ===> " , league_id, team_name
        return (None, error)

    league = League.objects.get(league_id=league_id)
    teams = league.team_set.all()    
    user = request.user

    if (not is_commisionar) and (league.password) and (password != league.password):
        error += "<br/> - Password did not match! ==> "
        print error, league.password, password
    if league.settings.number_of_teams <= len(teams):
        error += "<br/> - league is already full! ==>"
        print error, league.settings.number_of_teams, teams 
    if user in [t.user for t in teams]:
        error += "<br/> - you (%s) already have a team in this league! click inside the league to know about it."
        print error, user, [t.user for t in teams]
    if error:
        return (None, error)

    vendor_team_id = generate_random_id(4)
    vendor_user_id = 'xxyyzz'
    waiver_priority = 1
    division = ''
    t = Team(league=league,
             user=user,
             vendor_team_id=vendor_team_id,
             vendor_user_id=vendor_user_id,
             team_name=team_name,
             waiver_priority=waiver_priority,
             division=division,
             is_commisionar=is_commisionar,
             draft_pick_number=1)
    return (t,error)
