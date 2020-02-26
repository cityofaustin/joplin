from psycogreen.gevent import patch_psycopg
import os
DEPLOYMENT_MODE = os.environ.get('DEPLOYMENT_MODE')

worker_class = 'gevent'
workers = 4
# to stay under heroku limit of 20 connections
worker_connections = 4

pythonpath = "/app/joplin"
reload = True
#  see https://docs.gunicorn.org/en/stable/settings.html#max-requests
max_requests = 500
max_requests_jitter = 50
timeout = 190
preload = True
if DEPLOYMENT_MODE in ("LOCAL", "REVIEW"):
    timeout = 190
    loglevel = "DEBUG"


def post_fork(server, worker):
    patch_psycopg()
    worker.log.info("Made Psycopg2 run using gevent (for async stuff)")
