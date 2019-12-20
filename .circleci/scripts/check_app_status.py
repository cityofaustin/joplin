import subprocess
import re
import os
import sys
import json
import time
import heroku3


APPNAME = sys.argv[1]

HEROKU_KEY = os.getenv('HEROKU_KEY')
heroku = heroku3.from_key(HEROKU_KEY)


def check_app_status():
    print(f"Checking state of App {APPNAME}.")
    app = heroku.apps()[APPNAME]
    app_state = app.dynos()[0].state
    if (app_state == 'up'):
        print(f"App {APPNAME} is up. Ready to migrate.")
        return
    elif (app_state == 'starting') or (app_state == 'restarting'):
        print(f"App {APPNAME} is still starting up. Trying again")
        time.sleep(1)
        check_app_status()
    else:
        print(f"Error: App {APPNAME} is in state {app_state}")
        sys.exit(1)


check_app_status()
