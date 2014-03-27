from django.http import HttpResponse, HttpResponseRedirect
from django.template import Context, loader
from django.shortcuts import render, render_to_response
from django.contrib.auth import logout
from django.db.models import Count
from models import *
import pdb
import pprint
from data.models import *
from league.models import *
from team.models import *
from data.models import *
import app.helpers
import json
#@render_to_response('teams.html')
# class TeamsView(DetailView):
#     model = Teams
#     def get_teams_data():


def logged_in(request):
    return HttpResponseRedirect(request.GET.get('next', '/'))
    #return render(request, 'logged-in.html',
    #        {"data":
    #            pprint.pformat(request.session.items())})

def login_error(request):
    return render(request, 'login-error.html')

def log_out(request):
    logout(request)
    return HttpResponseRedirect('/')

def login_session(request):
    pip = request.session.get('partial_pipeline')
    user = {}
    backend = pip['kwargs']['backend']
    user['user_id'] = pip['kwargs']['user']['pk']
    user['social_user_id'] = pip['kwargs']['social_user']['pk']
    user['backend'] = pip['backend']
    
    if backend.name=='yahoo':
        user['username'] = pip['kwargs']['username']
        user.update(pip['kwargs']['details'])
    elif backend.name=='facebook':
        user.update(pip['kwargs']['response'])
    user['name'] = user['first_name']
    user['avatar'] = pip['kwargs']['avatar']
    user['ppipe'] = pip
    # TODO: check if there is no avatar, then add a default silhouette.
    request.session['user'] = user
    return HttpResponseRedirect('/complete/' + user['backend'])


def home(request):
    context = app.helpers.user_template_dict(request)
    if context:
        context['next_page'] = request.get_full_path
        context['providers'] = ['facebook', 'yahoo', 'google', 'github']
    #context['debug'] = pprint.pformat(request.session.items())
    #context['debug'] += '\n' + \
    #        pprint.pformat(app.helpers.user_template_dict(request))
        return render(request, 'index.html', context)
    else:
	return log_out(request)

