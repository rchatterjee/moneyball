from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.template import Context, loader
from django.shortcuts import render, render_to_response

def index(request):
    return HttpResponse("Pro-team index.")

def info(request, team_id):
    return HttpResponse("Pro-team (%s) info." % team_id)

def players(request, team_id):
    return HttpResponse("Pro-team (%s) players." % team_id)
