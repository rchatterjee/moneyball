import xml.etree.ElementTree as ET
import sys
import xmltodict

xmlns = '{http://fantasysports.yahooapis.com/fantasy/v2/base.rng}'
class YahooData:
    base_user_url = 'http://fantasysports.yahooapis.com/fantasy/v2/users;use_login=1'
    season = '2012'
    game_type = 'nfl'

    def get_content(self, url, xmlpath):
        url = '/'.join([self.base_user_url, url])
        print url
        res = self.auth_response.provider.access(url)
        if res.status==200:
            xmlns = res.data.tag.split('}')[0]+'}'
            a = []
            for x in res.data.iter("%s%s" % (xmlns, xmlpath[0])):
                a.append([x.find('%s%s' % (xmlns,y)).text for y in xmlpath[1]] )
            return a
        return None


    def __init__(self, auth_response):
        self.auth_response = auth_response
        game_list = self.get_content(url='games', xmlpath=['game', ['season', 'code', 'game_key']])
        assert game_list
        game_key = filter(lambda x: x[0]==self.season and x[1]==self.game_type, game_list)[0][2]
        print game_key, locals()
        
        leagues = self.get_content( 'games;game_keys={game_key}/leagues'.format(**locals()), ['league', ['league_key', 'name']])
        
        teams = self.get_content( 'games;game_keys={game_key}/teams'.format(**locals()), ['team',['team_key', 'name']])
        
        res = self.auth_response.provider.access('http://fantasysports.yahooapis.com/fantasy/v2/league/%s/players' % (leagues[0][0]))
        n=0
        print "Just before Entering whileLoop:", leagues, res.status, res.msg
        while( False and res.status==200 ): # done downloading..:P
            a = res.content
            dt = xmltodict.parse(a, namespaces={xmlns:None})
            dt = dt['fantasy_content']['league']['players']
            if not dt: break
            else: dt = dt['player']
            n += len(dt)
            for p in dt:
                #print p
                T = YahooTeam(team_key = p[u'editorial_team_key'],
                              team_full_name = p[u'editorial_team_full_name'],
                              team_abbr = p[u'editorial_team_abbr'])
                
                T.save()
                P = YahooPlayer(player_key= p[u'player_key'],
                                player_id = p[u'player_id'],
                                first_name= p[u'name'][u'ascii_first'],
                                last_name = p[u'name'][u'ascii_last'],
                                editorial_player_key= p[u'editorial_player_key'],
                                bye_week = p[u'bye_weeks']['week'],
                                editorial_team = T,
                                uniform_number= p[u'uniform_number'] or 0,
                                display_position= p[u'display_position'])
                P.save()
            res = self.auth_response.provider.access('http://fantasysports.yahooapis.com/fantasy/v2/league/%s/players;start=%d' % (leagues[0][0], n))
                

from django.db import models
from djangotoolbox.fields import ListField

class YahooTeam(models.Model):
    team_key = models.CharField(max_length=15, blank=False, primary_key=True) # editorial_team_key
    team_full_name= models.CharField(max_length=100) # editorial_team_full_name
    team_abbr = models.CharField(max_length=4)  # </editorial_team_abbr>
    

class YahooPlayer(models.Model):
    player_key= models.CharField(max_length=20, blank=False) # player_key
    player_id = models.IntegerField(primary_key=True, null=False) # player_id
    first_name= models.CharField(max_length=50) # ascii_first
    last_name = models.CharField(max_length=50, null=True) # ascii_last
    editorial_player_key= models.CharField(max_length=20, blank=False) # editorial_player_key
    editorial_team = models.ForeignKey(YahooTeam)
    bye_week =  ListField() # week
    uniform_number=models.IntegerField() # uniform_number
    display_position= models.CharField(max_length=2) # </display_position>

        
