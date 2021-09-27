#!/bin/bash
NAME="exp_taste"
DJANGODIR="/usr/local/src/exp_taste/"
SOCKFILE="/usr/local/src/exp_taste/run/gunicorn.sock"
USER=exp_taste_user
GROUP=webapps
NUM_WORKERS=3
TIMEOUT=120
DJANGO_SETTINGS_MODULE=config.settings.production
DJANGO_WSGI_MODULE=config.wsgi

echo "Starting $NAME as `whoami`"

# Activate the virtual environement
cd $DJANGODIR
source /usr/local/src/env/exp_taste/bin/activate

export DJANGO_SETTINGS_MODULE=$DJANGO_SETTINGS_MODULE
export PYTHONPATH=$DJANGODIR:$PYTHONPATH

# Create the run directory if it doesn't exist
RUNDIR=$(dirname $SOCKFILE)
test -d $RUNDIR || mkdir -p $RUNDIR

# Start you Django Unicorn 
# Programs meant to be run under supervisor should not
# daemonize themselves.
# (do not use --daemon)

exec /usr/local/src/env/exp_taste/bin/gunicorn ${DJANGO_WSGI_MODULE}:application \
    --name $NAME \
    --workers $NUM_WORKERS \
    --timeout $TIMEOUT \
    --user=$USER --group=$GROUP \
    --bind 127.0.0.1:8001 \
    --log-level=warning \
    --log-file=-

