#!/usr/bin/python
# -*- coding: utf-8 -*-

import sqlite3 as lite
import sys

con = None

try:
    con = lite.connect('test.db')
    
    cur = con.cursor()    
    cur.execute('SELECT SQLITE_VERSION()')
    cur.execute("CREATE TABLE NFL_DATA(PID VARCHAR, TID VARCHAR, Position CHAR(2), Week INT, Season INT, Rating REAL, QB_Comp INT, QB_Comp_Attempt INT, QB_Yds INT,QB_Y_by_A REAL, QB_Long INT, QB_Int,QB_TD,QB_Sack,QB_SackYds,RB_Run Att,RB_Yds,RB_Y/A,RB_Longest,RB_TD,WR_Rec,WR_Tgt,WR_Yds,WR_Y/R,WR_Lng,WR_TD,K_0-19,K_20-29,K_30-39,K_40-49,K_50+,K_FGM,K_FGA,K_Pct,K_Lng,K_XPM,K_XPA,K_Pct,K_Pts,D_TD,D_INT,D_FR,D_SCK,D_SFTY,D_BLK,D_PA,Fum,FumL
)")    
    data = cur.fetchone()
    
    print "SQLite version: %s" % data                
    
except lite.Error, e:
    
    print "Error %s:" % e.args[0]
    sys.exit(1)
    
finally:
    
    if con:
        con.close()
