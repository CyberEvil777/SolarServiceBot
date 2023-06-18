#!/bin/sh

python "manage.py" collectstatic --noinput

python "manage.py" migrate --noinput

gunicorn -c "gunicorn.conf.py" src.wsgi:application
