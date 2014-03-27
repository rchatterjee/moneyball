from django.shortcuts import render
import app

# Create your views here.
def index(request):
    context = app.helpers.user_template_dict(request)
    context.update({'next_page' : request.get_full_path })
	#{"data": pprint.pformat(request.session.items())})
    return render(request, 'settings.html', context)
