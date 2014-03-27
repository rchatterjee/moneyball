from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.template import Context, loader
from django.shortcuts import render, render_to_response

def index(request):
    return HttpResponse("Pro-player index.")

def info(request, player_id):
    return HttpResponse("Pro-player (%s) info." % player_id)
