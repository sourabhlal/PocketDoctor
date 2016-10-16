import os
import sys
import json

import requests
from flask import Flask, request, session
from twilio import twiml

# The session object makes use of a secret key.
SECRET_KEY = 'a secret key'
app = Flask(__name__)
app.config.from_object(__name__)

@app.route('/')
def hello_world():
    return 'Hello, World!'

def log(message):  # simple wrapper for logging to stdout on heroku
    print str(message)
    sys.stdout.flush()

@app.route("/sms", methods=['GET', 'POST'])
def sms_reply():

	# Increment the counter
    counter = session.get('counter', 0)
    counter += 1

    # Save the new counter value in the session
    session['counter'] = counter
    from_number = request.values.get('From')
    message = '{} has messaged {} {} times.' \
        .format(from_number, request.values.get('To'), counter)


    """Respond to incoming calls with a simple text message."""
    # Start our TwiML response
    resp = twiml.Response()

    # Add a message
    resp.message(message)

    return str(resp)

if __name__ == '__main__':
    app.run(debug=True)