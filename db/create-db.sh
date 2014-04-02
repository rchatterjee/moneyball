#!/bin/bash

set -x
rm -rf db.sqlite3
(cd ..; python manage.py syncdb --noinput)
(cd ..; python manage.py migrate)
./dump2sqlite.sh mysql_sqlite3.sql | sqlite3 db.sqlite3
./update_yahoo_id.sh | sqlite3 db.sqlite3
python agg-stats.py | sqlite3 db.sqlite3
