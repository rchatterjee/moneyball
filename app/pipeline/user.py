import json
from django.http import HttpResponse, HttpResponseRedirect
import urllib2
from app.models import UserExtraData
import pdb
import urllib
import pprint

FB_GRAPH_DP = \
"http://graph.facebook.com/%s?fields=id,picture.width(100).height(100),location"

def update_user(social_user, pic, loc, gender, link):
    (e, created) = UserExtraData.objects.get_or_create(
            user=social_user.user,
            defaults={"profile_logo": pic, "location": loc,
                "gender": gender, "profile_link": link})
    if not created:
        e.profile_log = pic
        e.location = loc
        e.gender = gender
        e.profile_link = link
    e.save()
    return

def extract_picture(data):
    url = ''
    try:
        url = data['picture']['data']['url']
    except:
        pass
    return url

def extract_location(data):
    loc = ''
    try:
        loc = data['location']['name']
    except:
        pass
    return loc

def extract_gender(data):
    g = ''
    try:
        g = data[u'gender']
        if g == u'male':
            g = 'M'
        elif g == u'female':
            g = 'F'
        else:
            g = '-'
    except:
        pass
    return g

def extract_profile_link(data):
    u = ''
    try:
        u = data[u'link']
        # XXX: Unicode string.
    except:
        pass
    return u

def extra_data(backend, response, user, *args, **kwargs):
    data = ''
    pic = ''
    location = ''
    if backend.name == "facebook":
        try:
            url = FB_GRAPH_DP % response['id']
            data = urllib2.urlopen(url).read()
            data = json.loads(data)
            pic = extract_picture(data)
            location = extract_location(data)
        except StandardError:
            pass
    else:
        raise ValueError()
    gender = extract_gender(response)
    link = extract_profile_link(response)
    update_user(kwargs['social_user'], pic, location, gender, link)
    #return HttpResponse('<pre>' + pprint.pformat(data) + '</pre>')
    return {'avatar': pic}

def session_save(backend, response, *args, **kwargs):
    return HttpResponseRedirect('/login-session')
