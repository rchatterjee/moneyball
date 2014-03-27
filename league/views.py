from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.template import Context, loader
from django.shortcuts import render, render_to_response
from league.models import *
import app
import string, random


def index(request):
    if request.method == 'POST':
        return HttpResponseRedirect('create/')
    context = app.helpers.user_template_dict(request)
    context['next_page'] = request.get_full_path
    context['providers'] = ['facebook', 'yahoo', 'google', 'github']
    return render(request, 'mock.html', context)


def generate_random_id(n = 6): 
    chars = string.ascii_uppercase + string.digits
    return ''.join([random.choice(chars) for x in xrange(n)])
                        

def create(request):
    print request.POST
    error = ''
    name = request.POST.get('leagueName', '');
    vendor = Vendor.objects.get(name='fantasyfans')
    if not vendor:
        error = "%sI doubt there is any vendor with this id %s" % (error, vendor)
    league_id = generate_random_id()
    team_count = int(request.POST.get('teamCount', '0'));
    settings = League_Settings(number_of_teams=team_count)
    print settings
    league_owner = request.user
    league = League(name=name, vendor=vendor, league_id=league_id, 
                    league_owner=league_owner, settings=settings)
    if league.save():
        return HttpResponse("Created LEAGUE page. with this info, %s" % ( str(league) ))
    else:
        return HttpResponse("<alert>Sorry Dude! something is messed up</alert><br/><b>ERROR</b> - {error}".format(error=error))
    

def league(request, league_id):
    response = "League (%s) page."
    return HttpResponse(response % league_id)


def join(request, league_id):
    return HttpResponse("Join league id (%s)." % league_id)
