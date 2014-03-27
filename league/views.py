from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.template import Context, loader
from django.shortcuts import render, render_to_response

def index(request):
    return HttpResponse("Leagues index page to list public leagues.")

def create(request):
    return HttpResponse("Create LEAGUE page.")

def league(request, league_id):
    response = "League (%s) page."
    return HttpResponse(response % league_id)

def join(request, league_id):
    return HttpResponse("Join league id (%s)." % league_id)
