import pdb
import os
DEPLOYMENT_MODE = os.environ.get('DEPLOYMENT_MODE')
print("WE ARE IN DEPLOYMENT MODE!!!", DEPLOYMENT_MODE)


pythonpath = "/app/joplin"
reload = True
max_requests = 100
max_requests_jitter = 50
timeout = 90
if DEPLOYMENT_MODE in ("LOCAL", "REVIEW"):
    timeout = 190
    loglevel = "DEBUG"
