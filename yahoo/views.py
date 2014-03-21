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

from yahoo_data import YahooData 

def login(request, provider_name):
    url = 'http://fantasysports.yahooapis.com/fantasy/v2/league/273.l.421159/players;start=25'
    response = HttpResponse()
    result = authomatic.login(DjangoAdapter(request, response), provider_name)
    if result:
        response.write('<a href="..">Home</a>')
        if result.error:
            response.write('<h2>Damn that error: {}</h2>'.format(result.error.message))
        elif result.user:
            y = YahooData(result)
            data = result.provider.access(url)
            # print data.content[:1000]
            open('out.txt', 'w').write(data.content)
            response.write('<h2>data.data:<h2><p>{}<p>'.format(data.read()))
            
            if not (result.user.name and result.user.id):
                result.user.update()
            response.write('<h1>Hi {}</h1>'.format(result.user.name))
            response.write('<h2>Your id is: {}</h2>'.format(result.user.id))
            response.write('<h2>Your email is: {}</h2>'.format(result.user.email)) 
            response.write('<h3>Your Info: %s' % vars(result))
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

