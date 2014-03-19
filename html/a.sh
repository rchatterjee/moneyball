#!/usr/bin/bash
sed -n 's/src\="img\/\(.*\).jpg/src\="{% static "img\/\1\.jpg" %}"/g' ../ffball/templates/base.html