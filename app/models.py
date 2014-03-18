from django.db import models
from django.contrib.auth.models import User

class UserExtraData(models.Model):
    user = models.OneToOneField(User)
    profile_logo = models.CharField(max_length=2000)
    GENDER_CHOICES = (
        ('-', 'Not defined'),
        ('M', 'Male'),
        ('F', 'Female'),
    )
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    profile_link = models.CharField(max_length=2000, choices=GENDER_CHOICES)
    location = models.CharField(max_length=256)
    email = models.CharField(max_length=256)
