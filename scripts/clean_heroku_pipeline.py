import os
import pdb
import heroku3
from datetime import datetime, timezone, timedelta
import logging
import http
http.client.HTTPConnection.debuglevel = 1
logging.basicConfig()  # you need to initialize logging, otherwise you will not see anything from requests
logging.getLogger().setLevel(logging.INFO)
requests_log = logging.getLogger("requests.packages.urllib3")
requests_log.setLevel(logging.INFO)
requests_log.propagate = True


"""
cmd refrences:
https://github.com/martyzz1/heroku3.py
"""
# TODO: import key from env variable, atm I just pasted mine in
HEROKU_KEY = os.getenv('HEROKU_KEY')
heroku = heroku3.from_key(HEROKU_KEY)


def define_date_threshold(days_ago):
    threshold = datetime.now(timezone.utc) - timedelta(days=days_ago)
    return threshold


def scale_apps(app_list, dynos):
    """
    scales dynos to 0, they stay in pipeline but don't cost anything,
    can be restarted easily
    """
    for app in app_list:
        app.process_formation()['web'].scale(0)


def exterminate(app_list):
    """
    this irreversably destroys the app
    ( though I'm pretty sure our CircleCI process would just build another one)
    """
    for app in app_list:
        app.delete()


"""
TODO: write these into functions and call, for now call from the command line
eg. exterminate(filtered_joplin_apps) or scale_apps(filtered_joplin_apps, 0)
"""
joplin_apps = [app for app in heroku.apps() if app.name.startswith('joplin-pr')]
filtered_joplin_apps = [app for app in joplin_apps if app.updated_at < define_date_threshold(60)]
