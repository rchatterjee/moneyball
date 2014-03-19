def user_template_dict(request):
    r = {}
    r['logged_in'] = is_logged_in(request)
    if not r['logged_in']:
        return r
    r['user'] = request.session['user']
    return r

def is_logged_in(request):
    if request.user.is_authenticated():
        return True
    return False
