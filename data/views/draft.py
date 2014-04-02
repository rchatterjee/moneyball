import json
import time

from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.template import Context, loader
from django.shortcuts import render, render_to_response
from django.core import serializers
from league.models import League
from django.utils import timezone

def updates(request, league_id):
    if not request.user.is_authenticated():
        pass
    r = {'league_id': league_id}
    try:
        l = League.objects.get(league_id = league_id)
        if l.draft_timeout:
            t = time.mktime(l.draft_timeout.timetuple())*1000
        else:
            t = l.draft_timeout
        r.update({'current': l.draft_current_id,
                   'timeout': t})
        last_trid = request.GET['last_transaction']
        adde_pids, last_trid = l.get_transactions_since(last_trid)
        if adde_pids:
            r.update({'remove-pid': adde_pids, 'last_transaction': last_trid})
    except League.DoesNotExist:
        pass
    return HttpResponse(json.dumps(r),
            content_type="application/json")
