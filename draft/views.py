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
from ffball.settings import errors
# Create your views here.


def join_league(request):
    t = create_team(request,0)
    print t, errors
    if t and not t.save():
        return HttpResponseRedirect( '/draftroom/%s' % t.league.league_id )
    else:
        return HttpResponseRedirect( '/mockdraft' );

def mock_draft(request):
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


def draft_room(request, draft_room_id):
    context = app.helpers.user_template_dict(request)
    context['next_page'] = request.get_full_path
    if request.method == "GET":
        context['draft_order'] = get_draft_order(draft_room_id)
    elif request.method == 'POST':
        d = request.POST.getlist('draft_order')
        set_draft_order(draft_room_id, d)
    myLeague = League.objects.filter(league_id = draft_room_id)
    context['me'] = request.user
    context['myLeague'] = myLeague
    print myLeague
    return render(request, 'draftroom.html', context)


def get_draft_order(draft_room_id):
    l = League.objects.get(league_id=draft_room_id)
    d = [None for x in range(l.settings.number_of_teams)]
    teams = l.team_set.all()
    for t in teams:
        d[t.draft_pick_number-1] = t
    return d


def set_draft_order(draft_room_id, d_list):
    # http://stackoverflow.com/questions/18045867/post-jquery-array-to-django
    for i,t in enumerate(d_list):
        if t<=0:
            continue
        t = Team.objects.get(id=i)
        t.draft_pick_number = i+1
        t.save()
    return True




def draft(request, draft_id=0):
    context = app.helpers.user_template_dict(request)
    context['next_page'] = request.get_full_path
    context['me'] = request.user
    return render(request, 'draft.html', context)

