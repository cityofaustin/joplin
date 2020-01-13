import os
DEPLOYMENT_MODE = os.environ.get('DEPLOYMENT_MODE')

worker_class = 'gevent'

pythonpath = "/app/joplin"
reload = True
#  see https://docs.gunicorn.org/en/stable/settings.html#max-requests
max_requests = 100
max_requests_jitter = 50
timeout = 190
preload = True
if DEPLOYMENT_MODE in ("LOCAL", "REVIEW"):
    timeout = 190
    loglevel = "DEBUG"
