#!/bin/bash

set -x

if [ $# -lt 1 ];
then
    echo "Give the app name you want to delete."
    exit;
fi

app=$1
sqlite3 db/db.sqlite3 .dump | grep "INSERT INTO \"${app}_" > .t.sql
# cat .t.sql
python manage.py sqlclear $app | sqlite3 db/db.sqlite3
python manage.py syncdb
sqlite3 db/db.sqlite3 < .t.sql
# rm .t.sql
