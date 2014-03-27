from django.shortcuts import render
from django.http import HttpResponse
import re
from django.contrib.auth.models import User
from team.models import Team


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
