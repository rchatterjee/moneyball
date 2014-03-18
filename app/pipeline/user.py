import json
from django.http import HttpResponse, HttpResponseRedirect
import urllib2
from app.models import UserExtraData
import pdb

FB_GRAPH_DP = \
"http://graph.facebook.com/%s?fields=picture.height(100).width(100)"

def update_logo(social_user, url):
    (e, created) = UserExtraData.objects.get_or_create(
            user=social_user.user,
            defaults={"profile_logo": url})
    if not created:
        e.profile_log = url
    e.save()
    return

def extra_data(backend, response, user, *args, **kwargs):
    data = ''
    if backend.name == "facebook":
        try:
            url = FB_GRAPH_DP % response['id']
            data = urllib2.urlopen(url).read()
            data = json.loads(data)['picture']['data']['url']
            update_logo(kwargs['social_user'], data)
        except StandardError:
            pass
    else:
        raise ValueError()
    return {'avatar': data}

def session_save(backend, response, *args, **kwargs):
    return HttpResponseRedirect('/login-session')
