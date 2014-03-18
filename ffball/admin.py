from django.contrib import admin
from ffball import models as ffm

admin.site.register(ffm.Team)
admin.site.register(ffm.Stat)
admin.site.register(ffm.Player)

