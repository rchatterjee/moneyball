from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.template import Context, loader
from django.shortcuts import render, render_to_response
from league.models import *
from django.db.models import Count
import app
import string, random
from team.models import Team

def index(request):
    context = app.helpers.user_template_dict(request)
    if not context: context = {}
    return HttpResponse("<h1> In Construction </h1>")


def generate_random_id(n = 6): 
    chars = string.ascii_uppercase + string.digits
    return ''.join([random.choice(chars) for x in xrange(n)])


def create(request):
    print request.POST
    error = ''
    name = request.POST.get('leagueName', '');
    vendor = Vendor.objects.get(name='moneyball')
    password = request.POST.get('entryKey', '')
    number_of_teams = request.POST.get('teamCountName', 10)
    league_type = request.POST.get('leagueTypeName', 'STD')
    draft_type = request.POST.get('draftTypeName', 'S')
    draft_date =request.POST.get('draftDateName', '')

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
    league = League(name=name, vendor=vendor, password=password, 
                    league_id=league_id, league_owner=league_owner, 
                    settings=settings)
    error = 'ERROR@!'
    if not league.save():
        from team.views import create_team
        t, error = create_team(request, 1, league_id)
        if t and not t.save():
            return HttpResponseRedirect( '/draftroom/%s' % league_id )
        if league: league.delete()
    return HttpResponse("Something went wrong ==> <br/> %s" % error);
    

def league(request, league_id):
    response = "League (%s) page."
    return HttpResponse(response % league_id)
