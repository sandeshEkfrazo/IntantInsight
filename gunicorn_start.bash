#Prod----------------

#!/bin/bash


NAME="instantinsightz" 
DJANGODIR=/instantInsight/django/server
DJANGOENVDIR=/instantInsight/venv
SOCKFILE=/instantInsight/venv/run/gunicorn.sock 
USER=root  
GROUP=root   
NUM_WORKERS=3 
DJANGO_SETTINGS_MODULE=robas.settings
DJANGO_WSGI_MODULE=robas.wsgi  

echo "Starting $NAME as `whoami`"

# Activate the virtual environment
cd $DJANGODIR
source /instantInsight/venv/bin/activate
export DJANGO_SETTINGS_MODULE=$DJANGO_SETTINGS_MODULE
export PYTHONPATH=$DJANGODIR:$PYTHONPATH

# Create the run directory if it doesn't exist
RUNDIR=$(dirname $SOCKFILE)
test -d $RUNDIR || mkdir -p $RUNDIR

# Start your Django Unicorn
# Programs meant to be run under supervisor should not daemonize themselves (do not use --daemon)
exec ${DJANGOENVDIR}/bin/gunicorn ${DJANGO_WSGI_MODULE}:application \
  --name $NAME \
  --workers $NUM_WORKERS \
  --user=$USER --group=$GROUP \
  --bind=unix:$SOCKFILE \
  --log-level=debug \
  --log-file=-



#Dev----------------


#!/bin/bash


NAME="robas" 
DJANGODIR=/robas/django/server
DJANGOENVDIR=/robas/venv
SOCKFILE=/robas/venv/run/gunicorn.sock 
USER=root  
GROUP=root   
NUM_WORKERS=3 
DJANGO_SETTINGS_MODULE=robas.settings
DJANGO_WSGI_MODULE=robas.wsgi  

echo "Starting $NAME as `whoami`"

# Activate the virtual environment
cd $DJANGODIR
source /robas/venv/bin/activate
export DJANGO_SETTINGS_MODULE=$DJANGO_SETTINGS_MODULE
export PYTHONPATH=$DJANGODIR:$PYTHONPATH

# Create the run directory if it doesn't exist
RUNDIR=$(dirname $SOCKFILE)
test -d $RUNDIR || mkdir -p $RUNDIR

# Start your Django Unicorn
# Programs meant to be run under supervisor should not daemonize themselves (do not use --daemon)
exec ${DJANGOENVDIR}/bin/gunicorn ${DJANGO_WSGI_MODULE}:application \
  --name $NAME \
  --workers $NUM_WORKERS \
  --user=$USER --group=$GROUP \
  --bind=unix:$SOCKFILE \
  --log-level=debug \
  --log-file=-

#############################
