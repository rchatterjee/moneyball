from django.test import TestCase
from django_dynamic_fixture import G, get
from league.models import *
from league.views import generate_random_id
import random
# Create your tests here.

#league_sample = [
#    {'name' : 'Party@mojo 2013',
#     'league_id' : generate_random_id(6
     
def fill_league_db():
    names = ['party@mojo', 'ebabare', 'awesomsala', 'existantical', 'epar bangla opar bangla',
            'World of Girls']
    we = Vendor.objects.get(name='moneyball')
    for name in names:
        P = generate_random_id()
        if sum([ord(p) for p in P]) % 13 < 7:
            P = ''
        owner = random.choice(User.objects.all())
        l1 = G(League, vendor=we, name=name, 
               league_id=generate_random_id(), 
               password=P,
               league_owner = owner )
        print l1

            
    
if __name__ == '__main__':
    fill_the_db()
