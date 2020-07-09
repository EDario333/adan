#!/bin/bash 

source ../bin/activate
python manage.py makemessages -l es
python manage.py compilemessages
