from django.conf.urls import patterns, include, url
import ffball.views
from django.contrib import admin
admin.autodiscover()
# import yahoo.views

urlpatterns = patterns('',
    # Examples:
    # url(r'^blog/', include('blog.urls')),
#    url('', include('social.apps.django_app.urls', namespace='social')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'', include('social_auth.urls')),
    url(r'^$', ffball.views.home, name='home'),
    url(r'^logged-in/', ffball.views.logged_in, name='logged-in'),
    url(r'^login-error/', ffball.views.login_error, name='login-error'),
    url(r'^login-session/', ffball.views.login_session, name='login-session'),
    url(r'^logout/', ffball.views.log_out, name='logout'),
    url(r'^teams/', ffball.views.teams, name='teams'),
    url(r'^draft/', ffball.views.draft, name='draft'),
    url(r'^mock/', ffball.views.mock, name='mock'),
    url(r'^settings/', ffball.views.settings, name='settings'),
#    url(r'^login/(\w*)', yahoo.views.login, name='login'),  
#    url(r'^loginall/',   yahoo.views.loginall, name='loginall'),
)


from django.contrib.staticfiles.urls import staticfiles_urlpatterns
urlpatterns += staticfiles_urlpatterns()
