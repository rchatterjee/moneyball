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


position = ["QB", "RB", "WR", "TE", "DE", "DT", "NT", "LB", "CB", "S", "K", "P"]
position = ["S"]
# year from season_2001 to season_2013
# week from week1 to week15
base_url = "http://sports.yahoo.com/nfl/stats/byposition?conference=NFL&qualified=0&sort=49&"
for pos in position:
    fname = "yahoo_data_%s" % pos
    writein = open(fname, 'w')
    x=0.1
    for yr in range(2001,2014):
        for w in range(1,18):
            url = "%spos=%s&&year=season_%d&timeframe=Week%d"%(base_url, pos, yr, w)
            print url
            urlfile = urlopen(url)
            parse_n_print(urlfile, writein, w, yr)
            if x>1: time.sleep(x); x=1/x;
            x=2*x
    writein.close()
