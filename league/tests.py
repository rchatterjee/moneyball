from django.test import TestCase
from django_dynamic_fixture import G, get
from league.models import *
# Create your tests here.

def fill_league_db():
    we = Vendor.objects.get(name='moneyball')
    for i in range(5):
        l1 = G(League, vendor=we)
        print l1

            
    
if __name__ == '__main__':
    fill_the_db()
