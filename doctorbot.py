import os
import sys
import json
import string
import urllib

import diagnose

import requests
from flask import Flask, request, session
from twilio import twiml

import infermedica_api
api = infermedica_api.API(app_id='21794b8d', app_key='81f5f69f0cc9d2defaa3c722c0e905bf')

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

	# Get the message the user sent our Twilio number and user number
	body = request.values.get('Body', None)
	from_number = request.values.get('From')
	log(body)

	# Increment the counter
	counter = session.get('counter', 0)
	state = session.get('state', 0)
	pm = session.get('pm', 0)
	age = session.get ('age', -1)
	gender = session.get ('gender', -1) #male=0, female = 1
	diagnosis = session.get ('diagnosis',{})

	counter += 1

	#Parse body
	if pm == 1 or pm == 2:
		age = int(body)
	elif pm == 3:
		if body == "M":
			gender = 0
		else:
			gender = 1


	# Determine the right reply for this message
	if state == 0:
		#newbie
		if age == -1 and gender == -1:
			message = "Hi! I'm DoctorBot. I can help you diagnose any medical conditions you may be facing. To get started please tell me your age"
			pm = 1
		elif age == -1:
			message = "What is your age?"
			pm = 2
		elif gender == -1:
			message = "What is your gender? (Please respond with either 'M' or 'F' "
			pm = 3
	elif state == 1:
		message = "boom"

	#update state & save session
	if state == 0 and age!=-1 and gender!=-1:
		state = 1
		message = '{}, {}, {}, {}' \
		.format(from_number, state, gender, age)

	session['pm'] = pm
	session['state'] = state
	session['age'] = age
	session['gender'] = gender


	"""Respond to incoming calls with a simple text message."""
	# Start our TwiML response
	resp = twiml.Response()

	# Add a message
	resp.message(message)

	return str(resp)

if __name__ == '__main__':
	app.run(debug=True)