from django.http import HttpResponse
from django.template import Context, loader
from django.shortcuts import render, render_to_response
from models import *
import pdb
from historical_data_models import *

#@render_to_response('teams.html')
# class TeamsView(DetailView):
#     model = Teams
#     def get_teams_data():

#     return render(request, 'teams.html')

def home(request):
    return render(request, 'index.html')

def logged_in(request):
    return render(request, 'logged-in.html',
            {"data":
                request.session.items()})

def login_error(request):
    return render(request, 'login-error.html')

def login_session(request):
    pdb.set_trace()
    pip = request.session.get('partial_pipeline')
    user = {}
    user['user_id'] = pip['kwargs']['user']['pk']
    user['social_user_id'] = pip['kwargs']['social_user']['pk']
    user['backend'] = pip['backend']
    user['username'] = pip['kwargs']['response']['username']
    user['access_token'] = pip['kwargs']['response']['access_token']
    user['avatar'] = pip['kwargs']['avatar']
    # TODO: check if there is no avatar, then add a default silhouette.
    request.session['user'] = user
    return HttpResponseRedirect('/complete/' + user['backend'])

def teams(request):
    all_teams = [] #Team.objects.all():
    template  = loader.get_template('teams.html')
    context   = Context( {
            'teams' : all_teams
            })
    return HttpResponse(template.render(context))
