from django.http import HttpResponse, HttpResponseRedirect
from django.template import Context, loader
from django.shortcuts import render, render_to_response
from django.contrib.auth import logout
from models import *
import pdb
import pprint
from historical_data_models import *
import app.helpers
import json
#@render_to_response('teams.html')
# class TeamsView(DetailView):
#     model = Teams
#     def get_teams_data():


def logged_in(request):
    return render(request, 'logged-in.html',
            {"data":
                pprint.pformat(request.session.items())})

def login_error(request):
    return render(request, 'login-error.html')

def log_out(request):
    logout(request)
    return HttpResponseRedirect('/')

def login_session(request):
    pip = request.session.get('partial_pipeline')
    user = {}
    user['user_id'] = pip['kwargs']['user']['pk']
    user['social_user_id'] = pip['kwargs']['social_user']['pk']
    user['backend'] = pip['backend']
    user['username'] = pip['kwargs']['response']['username']
    user['firstname'] = pip['kwargs']['response']['first_name']
    user['name'] = user['firstname']
    user['access_token'] = pip['kwargs']['response']['access_token']
    user['avatar'] = pip['kwargs']['avatar']
    user['ppipe'] = pip
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
	

def draft(request):
    context = app.helpers.user_template_dict(request)
    context['next_page'] = request.get_full_path
    return render(request, 'draft.html', context)
	
def settings(request):
    context = app.helpers.user_template_dict(request)
    context['next_page'] = request.get_full_path
    return render(request, 'settings.html', context)


def home(request):
    context = app.helpers.user_template_dict(request)
    context['next_page'] = request.get_full_path
    #context['debug'] = pprint.pformat(request.session.items())
    #context['debug'] += '\n' + \
    #        pprint.pformat(app.helpers.user_template_dict(request))
    return render(request, 'index.html', context)

	
def mock(request):
    context = app.helpers.user_template_dict(request)
    context['next_page'] = request.get_full_path
    return render(request, 'mock.html', context)
	
	
def draftroom(request):
    context = app.helpers.user_template_dict(request)
    context['next_page'] = request.get_full_path
    return render(request, 'draftroom.html', context)

