def user_template_dict(request):
    r = dict()
    r['logged_in'] = is_logged_in(request)
    if not r['logged_in']:
        return r
    r['user'] = request.session['user']
    return r


def is_logged_in(request):
    if hasattr(request.user, 'is_authenticated') and request.user.is_authenticated():
        return True
    elif 'user' in request.session: return True
    return False
