from github_webhook import Webhook
from flask import Flask
import os, json

app = Flask(__name__)
webhook = Webhook(app, secret=os.getenv("GITHUB_WEBHOOK_SECRET_TOKEN"))

@app.route("/")
def hello_world():
    print('Hello World!')
    return "Hello World!"

# Define a handler for the "pull_request" event
@webhook.hook(event_type='pull_request')
def on_pull_request(data):
    print("There was a PR")
    print(json.dumps(data))

# Only needed for local development
# Zappa handles the "app" object directly
if __name__ == '__main__':
    app.run()
