import os
import sys
import json

import requests
from flask import Flask, request
from twilio import twiml

app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello, World!'

def log(message):  # simple wrapper for logging to stdout on heroku
    print str(message)
    sys.stdout.flush()

@app.route("/sms", methods=['GET', 'POST'])
def sms_reply():
    """Respond to incoming calls with a simple text message."""
    # Start our TwiML response
    resp = twiml.Response()

    # Add a message
    resp.message("The Robots are coming! Head for the hills!")

    return str(resp)

if __name__ == '__main__':
    app.run(debug=True)