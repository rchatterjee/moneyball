def user_template_dict(request):
    r = dict()
    r[u'logged_in'] = is_logged_in(request)
    if not r[u'logged_in']:
        return r
    try:
        r[u'user'] = request.session['user']
    except KeyError:
        return None;
    return r


def is_logged_in(request):
    if hasattr(request.user, 'is_authenticated') and request.user.is_authenticated():
        return True
    elif u'user' in request.session: return True
    return False
