from psycogreen.gevent import patch_psycopg
import os
import multiprocessing
DEPLOYMENT_MODE = os.environ.get('DEPLOYMENT_MODE')

worker_class = 'gevent'
workers = multiprocessing.cpu_count() * 2 + 1
keepalive = 20

pythonpath = "/app/joplin"

if DEPLOYMENT_MODE in ("STAGING", "PRODUCTION"):
    timeout = 190
    worker_connections = 500


if DEPLOYMENT_MODE in ("LOCAL", "REVIEW"):
    timeout = 500
    loglevel = "DEBUG"
    # to stay under heroku limit of 20 connections
    worker_connections = 100
    reload = True


def post_fork(server, worker):
    from gevent import monkey
    patch_psycopg()
    worker.log.info("Made Psycopg2 run using gevent (for async stuff)")
    monkey.patch_all()
