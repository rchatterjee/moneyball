from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
import pdb

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
