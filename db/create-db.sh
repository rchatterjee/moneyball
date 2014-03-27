#!/bin/bash

set -x
rm -rf db.sqlite3
(cd ..; python manage.py syncdb --noinput)
./dump2sqlite.sh mysql_sqlite3.sql | sqlite3 db.sqlite3
