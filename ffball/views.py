from django.http import HttpResponse, HttpResponseRedirect
from django.template import Context, loader
from django.shortcuts import render, render_to_response
from django.contrib.auth import logout
from models import *
import pdb
import pprint
from historical_data_models import *
import app.helpers

#@render_to_response('teams.html')
# class TeamsView(DetailView):
#     model = Teams
#     def get_teams_data():

#     return render(request, 'teams.html')
from authomatic import Authomatic
from authomatic.adapters import DjangoAdapter

from config import CONFIG

authomatic = Authomatic(config=CONFIG, secret='This is a really string')


def draft(request):
    return render(request, 'draft.html')

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
    return render(request, 'draft.html', context)
	
def settings(request):
    context = app.helpers.user_template_dict(request)
    return render(request, 'settings.html', context)

def login(request, provider_name):
    response = HttpResponse()
    result = authomatic.login(DjangoAdapter(request, response), provider_name)
    if result:
        response.write('<a href="..">Home</a>')
        if result.error:
            response.write('<h2>Damn that error: {}</h2>'.format(result.error.message))

        elif result.user:
            if not (result.user.name and result.user.id):
                result.user.update()
            response.write('<h1>Hi {}</h1>'.format(result.user.name))
            response.write('<h2>Your id is: {}</h2>'.format(result.user.id))
            response.write('<h2>Your email is: {}</h2>'.format(result.user.email)) 
            response.write('<h3>Your Info: %s' % vars(result.user))
    return response

           

def loginall(request):
    return HttpResponse('''
        Login with <a href="/login/fb">Facebook</a>.<br />
        Login with <a href="/login/tw">Twitter</a>.<br />
        <form action="/login/ya">
            <input type="text" name="id" value="me.yahoo.com" />
            <input type="submit" value="Authenticate With OpenID">
        </form>
    ''')


def home(request):
    context = app.helpers.user_template_dict(request)
    context['next_page'] = request.get_full_path
    #context['debug'] = pprint.pformat(request.session.items())
    #context['debug'] += '\n' + \
    #        pprint.pformat(app.helpers.user_template_dict(request))
    return render(request, 'index.html', context)
