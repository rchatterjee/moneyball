from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.template import Context, loader
from django.shortcuts import render, render_to_response
from league.models import *
from django.db.models import Count
import app
import string, random
from  league.models import *
from team.views import *
from team.models import Team
# Create your views here.


def joinleague(request):
    t, error = create_team(request,0)
    print t, error
    if t and not t.save():
        return HttpResponseRedirect( '/draftroom/%s' % t.league.league_id )
    else:
        return HttpResponse("Something went wrong ==> <br/> %s" % error);

def mockdraft(request):
    draftList = League.objects.filter(vendor__name = 'moneyball')
    draftList = draftList.annotate(teamCount=Count('team'))
    draftList = draftList.order_by('settings__draft_date','teamCount')
    context = app.helpers.user_template_dict(request)
    if context["logged_in"]:
        myTeamList = Team.objects.filter(user = request.user).only('league')
        context['myTeamList'] = myTeamList
    context['next_page'] = request.get_full_path
    context['providers'] = ['facebook', 'yahoo', 'google', 'github']
    context['draftList'] = draftList
    context['me'] = request.user
    return render(request, 'mock.html', context)


def draftroom(request, draftroom_id):
    context = app.helpers.user_template_dict(request)
    context['next_page'] = request.get_full_path
    context['me'] = request.user
    return render(request, 'draftroom.html', context)

def draft(request, draft_id=0):
    context = app.helpers.user_template_dict(request)
    context['next_page'] = request.get_full_path
    context['me'] = request.user
    return render(request, 'draft.html', context)

