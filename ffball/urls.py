from django.conf.urls import patterns, include, url
import ffball.views

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^blog/', include('blog.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'', include('social_auth.urls')),
    url(r'^$', ffball.views.home, name='home'),
    url(r'^logged-in/', ffball.views.logged_in, name='logged-in'),
    url(r'^login-error/', ffball.views.login_error, name='login-error'),
    url(r'^teams/', ffball.views.teams, name='teams'),    
)


from django.contrib.staticfiles.urls import staticfiles_urlpatterns
urlpatterns += staticfiles_urlpatterns()
