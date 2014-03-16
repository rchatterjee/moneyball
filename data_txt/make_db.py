#!/usr/bin/python
import os,sys

if len(sys.argv)<2:
    print sys.argv[0], "<CSVFile>"
    exit(1)

f = open(sys.argv[1])
colnames = ''
tablename = ''
print 'start transaction;'
for line in f:
    if not tablename:
        tablename = line.strip().split(',')[0].upper()
    elif not colnames:
        colnames = line.strip().upper()
    else:
        l = [ None if (x=='N/A') else x for x in line.strip().split(',') ]
        cmd = "insert into srgdb.%s (%s) values ( %s );" % ( tablename, colnames, ', '.join(["'%s'" % x if x else 'NULL' for x in l]) )
        print cmd;
print 'commit;'
