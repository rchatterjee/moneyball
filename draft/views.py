from django.http import HttpResponse, HttpResponseRedirect
from django.db.models import Count
import app, json
from team.views import *
from team.models import Team
from ffball.settings import errors
import random


errors=''
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
    if context and context["logged_in"]:
        myTeamList = Team.objects.filter(user = request.user).only('league')
        context['myTeamList'] = myTeamList
        context['me'] = request.user
    else:
        context={};
    context['next_page'] = request.get_full_path
    context['providers'] = ['facebook', 'yahoo', 'google', 'github']
    context['draftList'] = draftList
    context['random_league'] = random.choice([x.league_id for x in draftList[:10]])
    return render(request, 'mock.html', context)



def draft_room(request, draft_room_id):
    global errors
    context = app.helpers.user_template_dict(request)
    if not context:
        return HttpResponseRedirect('/')
    context['next_page'] = request.get_full_path
    context['draft_room_id'] = draft_room_id
    if request.method == "GET":
        context['draft_order'] = get_draft_order(draft_room_id)
    elif request.method == 'POST' and request.is_ajax():
        d = request.POST.get('draft_order', '')
        result = "error"
        if d and set_draft_order(json.loads(d)):
            result = "successful"
        to_json = {'result':result, 'errors' : errors}
        return HttpResponse(json.dumps(to_json), mimetype='application/json')
    else:
        s = request.POST
        if s and set_league_settings(draft_room_id, s):
            return HttpResponseRedirect('/draftroom/%s' % draft_room_id )
        else:
            return HttpResponse( "ERROR" + errors )
    myLeague = League.objects.filter(league_id = draft_room_id)
    thisLeague = myLeague[0]
    context['me'] = request.user
    context['thisLeague'] = thisLeague
    return render(request, 'draftroom.html', context)


def set_draft_order(d_list):
    # http://stackoverflow.com/questions/18045867/post-jquery-array-to-django
    for i,t in enumerate(d_list):
        t = int(t.split('-')[1])
        if t<=0:
            continue
        x = Team.objects.get(id=t)
        x.draft_pick_number = i+1
        x.save()
    return True


def get_draft_order(draft_room_id):
    l = League.objects.get(league_id=draft_room_id)
    d = [None for x in range(l.settings.number_of_teams)]
    teams = l.team_set.all()
#print [t.draft_pick_number for t in teams]
    for t in teams:
        try:
            d[t.draft_pick_number-1] = t
        except IndexError:
            fix_draft_order(teams, l.settings.number_of_teams, l.settings.number_of_teams, True)
            return get_draft_order(draft_room_id)
    return d

def fix_draft_order(teams, old_size, new_size, forced=False):
    if old_size>new_size: return True
    global errors
    if len(teams)>new_size and not forced: # ERROR
        errors += "you have more number of teams than current team size. Cannot Save!"
        return False;
    else:
        if forced: old_size = 16;
        td = [None for x in range(old_size)]
        for t in teams:
            td[t.draft_pick_number-1] = t
        td.reverse()
        for i in range(old_size - new_size):
            x = td.index(None)
            del td[x]
        assert len(td) == new_size
        td.reverse()
        for i, o in enumerate(td):
            if o:
                o.draft_pick_number = i+1
                o.save()
    return True


def set_league_settings(league_id, set_dict):
    l = League.objects.get(league_id=league_id)
    s = l.settings
    print( set_dict )
    s.draft_date = set_dict.get('draftDateName', s.draft_date)
    s.league_type  = set_dict.get('leagueTypeName', s.league_type);
    l.name  = set_dict.get('lName', l.name);
    s.seconds_per_pick = set_dict.get('pickTime', s.seconds_per_pick)
    old_number_of_teams = s.number_of_teams;
    s.number_of_teams = int(set_dict.get('teamCountName', s.number_of_teams))
    # team size has changed now do something with the teams
    # it already has
    if old_number_of_teams > s.number_of_teams:
        teams = l.team_set.all()
        if not fix_draft_order(teams, old_number_of_teams, s.number_of_teams):
            s.number_of_teams = old_number_of_teams
            return False;
    s.save()
    l.save()
    return True


def draft(request, draft_id):
    from dodraft import *
    context = app.helpers.user_template_dict(request)
    if not context or not context['logged_in']:
        return HttpResponseRedirect('/')
    myLeague = League.objects.filter(league_id = draft_id)
    thisLeague = myLeague[0]
    myTeamList = Team.objects.filter(user = request.user).only('league')
    context['next_page'] = request.get_full_path
    context['me'] = request.user
    context['thisLeague'] = thisLeague
    context['myTeamList'] = myTeamList
    context.update(populate_draft_page(draft_id, request.user))
    return render(request, 'draft.html', context)

