from django.db import models
from django.contrib.auth.models import User

class UserExtraData(models.Model):
    user = models.OneToOneField(User)
    profile_logo = models.CharField(max_length=2000)
