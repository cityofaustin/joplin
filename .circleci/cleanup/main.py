from github_webhook import Webhook
from flask import Flask
import os, json, re
import heroku3

app = Flask(__name__)
webhook = Webhook(app, secret=os.getenv("GITHUB_WEBHOOK_SECRET_TOKEN"))

# Handle uncaught 500 Internal Server Errors
def handle_internal_server_error(e):
    print(str(e))
    traceback.print_tb(e.__traceback__)

    status = {
        'status': 'error',
        'message': str(e)
    }
    return jsonify(status), 500
app.register_error_handler(500, handle_internal_server_error)

# Get connection to heroku api
heroku_conn = heroku3.from_key(os.getenv('HEROKU_KEY'))

@app.route("/")
def hello_world():
    print('Hello World!')
    return "Hello World!"

# Define a handler for the "pull_request" event
@webhook.hook(event_type='pull_request')
def on_pull_request(data):
    print(json.dumps(data))
    # TODO: is it actually called "merged"?
    # TODO: get a HEROKU_KEY
    if (data.action == "closed") || (data.action == "merged"):
        app_name = re.sub(r'-*$','', f"joplin-pr{data["head"]["ref"]}"[0:30])
        heroku_app = heroku_conn.apps()[app_name]
        print(f"Starting to deleting app {app_name}")
        heroku_app.delete()
        print(f"Successfully deleted app {app_name}")

# Only needed for local development
# Zappa handles the "app" object directly
if __name__ == '__main__':
    app.run()
