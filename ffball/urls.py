from django.conf.urls import patterns, include, url
import ffball.views
from django.contrib import admin
#import team
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^blog/', include('blog.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'', include('social_auth.urls')),
    url(r'', include('settings.urls'), name='settings'),
    url(r'^$', ffball.views.home, name='home'),
    url(r'', include('draft.urls'), name='draft'),
    url(r'^logged-in/', ffball.views.logged_in, name='logged-in'),
    url(r'^login-error/', ffball.views.login_error, name='login-error'),
    url(r'^login-session/', ffball.views.login_session, name='login-session'),
    url(r'^logout/', ffball.views.log_out, name='logout'),
    url(r'^league/', include('league.urls')),
    url(r'^data/', include('data.urls')),
    url(r'', include('team.urls')),
#    url(r'^login/(\w*)', yahoo.views.login, name='login'),  
#    url(r'^loginall/',   yahoo.views.loginall, name='loginall'),
)


from django.contrib.staticfiles.urls import staticfiles_urlpatterns
urlpatterns += staticfiles_urlpatterns()
