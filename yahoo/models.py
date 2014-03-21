from django.db import models
import authomatic 
# Create your models here.
def is_authenticated():
    print "\n---------Authenticaed Called-------------\n"
    return True
authomatic.core.User.is_authenticated = is_authenticated
