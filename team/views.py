from django.shortcuts import render
from django.http import HttpResponse
import re
from django.contrib.auth.models import User

redirect_map = { '' : index,
            'create/' : create,
             'delete/' : delete,
             'edit/'   : edit
}

def redirect(request, action):
    try:
        if not request.user.is_authenticated():
            raise KeyError;
    except KeyError:
        return HttpResponse("<error>Sorry! You dont look like an authorised user for this action.<error>")
    try:
        return redirect_map[action] ( request)
    except KeyError:
        m = re.match(r'\d+')
        if m:
            id = int(m.group(1))
            return desc(request, id)
    return HttpResponse("<error>Page Not Found.<error>")


def index(request):
    context = { 'teams': request.user.Teams }
    return HttpResponse("<h1>Teams:<h1>%s" % context['teams'])
    #return render(request, 'views.html', context);


def create(request):
    
    request.user.Team.create()
    pass

def delete(request):
    pass

def edit(request):
    pass


def desc(request, id):
    pass
