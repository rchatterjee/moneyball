from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.template import Context, loader
from django.shortcuts import render, render_to_response
from django.contrib.auth import logout
from models import *
import pdb
import pprint
import app.helpers
import json

#     return render(request, 'teams.html')
from authomatic import Authomatic
from authomatic.adapters import DjangoAdapter

from ffball.config import CONFIG

authomatic = Authomatic(config=CONFIG, secret='This is a really string')

def login(request, provider_name):
    response = HttpResponse()
    result = authomatic.login(DjangoAdapter(request, response), provider_name)
    if result:
        #response.write('<a href="..">Home</a>')
        if result.error:
            response.write('<h2>Damn that error: {}</h2>'.format(result.error.message))
        elif result.user:
            #data = result.provider.access(url)
            if not (result.user.name and result.user.id):
                result.user.update()
            print pprint.pformat(vars(result.user))
            print pprint.pformat(vars(request.session))
            request.session['user'] = result.user.to_dict()
            request.session['user']['avatar'] = result.user.picture
        return HttpResponseRedirect(request.GET.get('next', '/'))
    else:
        print "Sorry Authentication Failed! for ", provider_name
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

