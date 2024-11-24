#!/bin/sh
python manage.py migrate
# I know this command don't supposed to belong here but just for the convenience of TA grading.
#python manage.py loaddata data/polls-v4.json data/users.json data/votes-v4.json
python manage.py runserver 0.0.0.0:8000