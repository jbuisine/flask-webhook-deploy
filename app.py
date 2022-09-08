"""
Flask application routes
"""
import os
import json

from flask import Flask

# get configuration
config = None
with open("config.json") as f:
    config = json.load(f)

# initialize the flask app
app = Flask("webhook_app", static_folder='./web/static', template_folder='./web/templates')
app.secret_key = b''

@app.route('/')
def index():
    """
    Route which tracks webhook
    """
    return json.dumps(config)