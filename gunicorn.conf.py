import os
DEPLOYMENT_MODE = os.environ.get('DEPLOYMENT_MODE')

pythonpath = "/app/joplin"
reload = True

if DEPLOYMENT_MODE in ("STAGING", "PRODUCTION"):
    preload = True
    timeout = 190
    # see https://docs.gunicorn.org/en/stable/settings.html#max-requests
    max_requests = 100
    max_requests_jitter = 50
else:
    timeout = 190
    loglevel = "DEBUG"
    preload = True
