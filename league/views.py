from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from league.models import *
import string, random, app
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from team.models import Team


def index(request):
    context = app.helpers.user_template_dict(request)
    if not context: context = {}
    return HttpResponse("<h1> In Construction </h1>")


def generate_random_id(n = 6): 
    chars = string.ascii_uppercase + string.digits
    return ''.join([random.choice(chars) for x in xrange(n)])

@login_required
def delete(request):
    l_id = request.POST.get('id', 0)
    try:
        t = Team.objects.get(user=request.user, id=l_id)
        t.delete()
    except Team.DonotExist:
        messages.error(request, "The team you are trying to access is not under your realm! Sorry :P")


@login_required
def create(request):
    context = {'logged_in':1, 'user':request.user}
    if request.POST:
        print request.POST
        name = request.POST.get('leagueName', '');
        vendor = Vendor.objects.get(name='moneyball')
        password = request.POST.get('entryKey', '')
        number_of_teams = request.POST.get('teamCount', 10)
        league_type = request.POST.get('leagueType', 'STD')
        draft_type = request.POST.get('draftType', 'S')
        draft_date =request.POST.get('draftDateName', '')

        error = ''
        if not name:
            return HttpResponse("<alert>Sorry Dude! something is messed up</alert><br/><b>ERROR</b> - {error}".format(error=error))
        
        if not vendor:
            error = "%sI doubt there is any vendor with this id %s" % (error, vendor)

        league_id = generate_random_id()
        settings = League_Settings(number_of_teams=number_of_teams,
                                   league_type = league_type,
                                   draft_type = draft_type,
                                   draft_date = draft_date
                                   )
        print settings
        league_owner = request.user
        l = League(name=name, vendor=vendor, password=password,
                   league_id=league_id, league_owner=league_owner,
                   settings=settings)

        if not l.save():
            from team.views import create_team
            t = create_team(request, 1, league_id)
            print "Team: ",t , "ERROR:", error
            if t and not t.save():
                return HttpResponseRedirect( '/draftroom/%s' % league_id )
            else:
                l.delete()
        return HttpResponseRedirect('/mockdraft/');
    else:
        return render(request, 'draftroom.html', context)


    
@login_required
def leave(request):
    l_id = request.POST.get('leagueId', '')
    if l_id:
        l = League.objects.get(league_id=l_id)
        t = l.team_set.filter(user=request.user)
        if t: t.delete()
        else: messages.error("Could not delete!")
    HttpResponseRedirect(request.get_full_path, request.context)





def league(request, league_id):
    response = "League (%s) page."
    return HttpResponse(response % league_id)
