"""
Flask webhook application 
"""
import os
import json
import hmac
import hashlib

from flask import Flask, request

# get configuration
with open("config.json") as f:
    config = json.load(f)

# initialize the flask app
app = Flask("webhook_app", static_folder='./web/static', template_folder='./web/templates')
app.secret_key = bytes(f"{config['flask_secret']}", 'utf-8')

@app.route('/', methods=['POST'])
def index():
    """
    Route which tracks webhook
    """
    
    if verify_signature(request, config['webhook_secret']):
        
        print("Secret has been verified")
        print(f"Running custom command... {config['command']}")
        os.system(config['command'])
        return json.dumps({"message": "ok"})
    else:
        print("Unexpected secret")
        return json.dumps({"message": "error"})

def verify_signature(req, secret):
    """Compare secret signature

    Returns:
        {bool} -- if signature is ok or not
    """
    received_sign = req.headers.get('X-Hub-Signature-256').split('sha256=')[-1].strip()
    secret = secret.encode()
    expected_sign = hmac.HMAC(key=secret, msg=req.data, digestmod=hashlib.sha256).hexdigest()
    return hmac.compare_digest(received_sign, expected_sign)
