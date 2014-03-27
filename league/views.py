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

def mock(request):
    draftList = League.objects.filter(vendor__name = 'uwbadgers')
    draftList = draftList.annotate(teamCount=Count('team'))
    context = app.helpers.user_template_dict(request)
    context['next_page'] = request.get_full_path
    context['providers'] = ['facebook', 'yahoo', 'google', 'github']
    context['draftList'] = draftList
    return render(request, 'mock.html', context)


def draftroom(request):
    context = app.helpers.user_template_dict(request)
    context['next_page'] = request.get_full_path
    return render(request, 'draftroom.html', context)
