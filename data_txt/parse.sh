#!/bin/bash
fl=$1;
cut -d, -f1 $fl | sed 's/[_@]/,/g;' | sort -t, -k1 -u | awk -F, '
{
  date=$1; if(!lastdate) {lastdate = date; week=0}; 
  yr=substr(date, 0, 5); if(!season) season=yr; dist=date-lastdate; lastdate=date; 
  if (dist>5) week++; print yr","season","week","$0
}' 
