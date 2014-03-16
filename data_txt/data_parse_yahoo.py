#!/usr/bin/python

import os, sys
from bs4 import BeautifulSoup
from urllib2 import urlopen
import time

def parse_n_print(f, writein, week=1, year=2001):
    s = BeautifulSoup(f.read())
    div = s.find_all(id="yom-league-stats")
    table = div[0].find_all('table')[5]
    rows = table.find_all("tr")
    heading1 = filter(lambda x: x, [ h.text.strip() for h in rows[0].find_all("td") ])
    heading2 = filter(lambda x: x, [ h.text.strip() for h in rows[1].find_all("td") ])
    data = [ filter(lambda x: x, [ h.text.strip() for h in row.find_all("td") ]) for row in rows[2:] ]
    if week==1 and year==2001:
        writein.write('# %s\n' % ', '.join(heading1))
        writein.write('# %s\n' % ', '.join(heading2))
    writein.write("# Season:%d week:%d\n" % (year, week))
    for s in data: writein.write(', '.join(s) + "\n")


def espn_download():
    teams = ['ari', 'atl', 'bal', 'buf', 'car', 'chi', 'cin', 'cle', 
             'dal', 'den', 'det', 'gb', 'hou', 'ind', 'jax', 'kc', 
             'mia', 'min', 'ne', 'no','nyg', 'nyj', 'oak', 'phi', 
             'pit', 'sd', 'sf', 'sea', 'stl', 'tb', 'ten', 'wsh']
    x = 1
    for team in teams:
        ofname='raw_data/team_data_%s.csv' % team.upper()
        ofile = open(ofname, 'w')
        for yr in range(2002, 2014):
            base_url='http://espn.go.com/nfl/team/schedule/_/name/%s/year/%d'%(team, yr)
            urlfile = urlopen(base_url)
            s = BeautifulSoup(urlfile.read())
            #if x>1: time.sleep(x); x=1/x;
            table = s.find_all(class_='mod-content')[0]
            rows = table.find_all("tr")
            
            data = [ filter(lambda x: x, [ h.text.strip() for h in row.find_all("td") ]) for row in rows ]
            for r in data : 
                if len(r) <=2: ofile.write('#'+','.join(r)+'\n')
                elif r[2][:1] != '@': 
                    r[2] = r[2][2:]
                    ofile.write(','.join(r)+'\n')
        ofile.close()
        x += 1;
        if x >5: time.sleep(2); x=0



def download():
    position = ["QB", "RB", "WR", "TE", "DE", "DT", "NT", "LB", "CB", "S", "K", "P"]
    #position = ["QB", "RB", "WR", "TE", "DE", "DT"]
    # year from season_2001 to season_2013
    # week from week1 to week15
    base_url = "http://sports.yahoo.com/nfl/stats/byposition?conference=NFL&qualified=0&sort=49&"
    for pos in position:
        fname = "yahoo_data_%s" % pos
        writein = open(fname, 'a')
        x=0.1
        for yr in range(2013,2014):
            for w in range(17,18):
                url = "%spos=%s&&year=season_%d&timeframe=Week%d"%(base_url, pos, yr, w)
                print url
                urlfile = urlopen(url)
                parse_n_print(urlfile, writein, w, yr)
                if x>1: time.sleep(x); x=1/x;
                x=2*x
        writein.close()

def ArrToCSVstring(arr):
    if not arr: return ''
    return ','.join([str(a) for a in arr])


def getAllPlayers():
    position = ["QB", "RB", "WR", "TE", "K"]    
    players = {}
    counter = {}
    for p in position:
        f = open('yahoo_data_%s' % p);
        for line in f:
            if line[0]!='#':
                a = line.strip().split(',')
                name, team = a[0], a[1]
                name = "%s,%s" %(name, p)
                if name in players:
                    if team not in players[name]:
                        players[name].append(team);
                    # Check past results
                else:
                    players[name] = [team]
    for name, p in players.items():
        pos = name.split(',')[1]
        if len(pos)==1: pos+=pos
        k = "%3s%2s" % (p[-1], pos)
        try: counter[k] += 1
        except KeyError: counter[k] = 1
        pid = "%s%03d" % (k, counter[k])
        print "%s,%s,%s,<%s>" % ( pid, name.replace("'", "\\'"), p[-1], '|'.join(p[:-1]))

                               
 
def modifyDataFiles():
    # multiple players with same name and position
    conflicted_players = {"Adrian Peterson": {"CHI":"CHIRB012", "MIN":"MINRB014"}, 
                          "Zach Miller":{"OAK,SEA":"SEATE006", "JAC":"JACTE016"}, 
                          "Steve Smith":{"NYG,PHI,STL":"STLWR009", "CAR":"CARWR023"}
                          }
    
    position = ["QB", "RB", "WR", "TE", "DE", "DT", "NT", "LB", "CB", "S", "K", "P"]
    position = ["QB", "RB", "WR", "TE", "K"]


    for p in position:
        players={}
        fplayrer = open('AllPlayers.csv')
        for i, line in enumerate(fplayrer):
            if i<2: continue;
            l = line.split(',')
            if l[2]==p:
                players[l[1]] = l[0]
        f = open('yahoo_data_%s' % p).readlines();
        wf = open('yahoo_data_%s.csv' % p, 'w')
        wf.write(f[0])
        f[1] = f[1].replace('Name', 'PID' )
        f[1] = f[1].replace('Team,G', 'TID,Season,Week' )
        wf.write(f[1])
        season,week = 0,0
        for n,line in enumerate(f[2:]):
            if line.startswith('# Season:'):
                line = line.strip().split()
                season,week = int(line[1].split(':')[1]), int(line[2].split(':')[1])
                continue
            a = line.strip().split(',')
            try:
               #getting PID
                a[0] = a[0].replace("'", "\\'")
                pid=''
                if a[0] in conflicted_players:
                    for x,y in conflicted_players[a[0]].items():
                        if a[1] in x.split(','): pid = y; break
                else:
                    pid = players[a[0]]
                if not pid: print "ERROR!!!!!", a;
                a[0] = pid
            except KeyError:
                print a[0], 'not in the the players list. CHECK!!!!'

            a[2] = str(season)
            a.insert(3, str(week));
            wf.write(','.join(a)+'\n')
        wf.close()

def parse_nfl_pbp_data():
    fl_name = './raw_data/2002_nfl_pbp_data.csv'
    week = 1;
    for line in open(fl_name):
        if not line.strip(): continue
        d = line.split()[0]
        if d[:2] != '20': continue
        d = d.split('_')
        yr = d[0];
        t1, t2 = d[1].split('@')
        
#modifyDataFiles()
#download()
#getAllPlayers();
espn_download()
