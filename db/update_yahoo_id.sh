#!/bin/bash

cd $(pwd | sed 's/\(.*moneyball\)\/\(.*\)$/\1/g')
cd data_txt
positions="QB RB TE WR K DE"
for pos in $positions
do
    join -t ":" -1 1 -2 1 -o 1.2,2.2 \
	<(grep ",$pos," AllPlayers.csv        | awk -F, '{printf "%s,%s,%s:%s\n",$2,$3,$4,$1}' | sort -t: -k1) \
	<(grep ".$pos," Allplayer_yahooid.csv | awk -F, '{printf "%s,%s,%s:%s\n",$2,$3,$4,$1}' | sort -t: -k1) \
	| awk -F: '{printf "UPDATE PLAYERS SET YAHOOID=\"%s\" WHERE PID=\"%s\";\n", $2, $1 }'
done
