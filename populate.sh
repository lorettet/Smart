#!/bin/bash

rm api/migrations/* db.sqlite3
./manage.py makemigrations api
./manage.py migrate
sqlite3 db.sqlite3 ".read populate.sql"
./manage.py shell -c "from django.contrib.auth.models import User; User.objects.create_superuser('admin', '', '123')"

./manage.py runserver