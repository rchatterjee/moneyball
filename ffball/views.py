from django.http import HttpResponse
from django.template import Context, loader
from django.shortcuts import render, render_to_response
from models import *
from historical_data_models import *

#@render_to_response('teams.html')
# class TeamsView(DetailView):
#     model = Teams
#     def get_teams_data():

#     return render(request, 'teams.html')

def home(request):
    return render(request, 'index.html')

def logged_in(request):
    return render(request, 'logged-in.html')

def login_error(request):
    return render(request, 'login-error.html')

def teams(request):
    all_teams = [] #Team.objects.all():
    template  = loader.get_template('teams.html')
    context   = Context( {
            'teams' : all_teams
            })
    return HttpResponse(template.render(context))
