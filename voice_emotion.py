from flask import Flask
from flask_ask import Ask, statement, question, session
import requests
import time
import unidecode
import json
import random

app = Flask(__name__)
ask = Ask(app, '/')

@app.route('/')
def homepage():
    return "Hello"

@ask.launch
def record_voice():
    original = "Hello there. I'm Peanuts, your personalized emotional assistant. How was your day?"
    re_message = "I didn't understand that. Try again, this time prefacing your statement with my name, Peanuts."
    return question(original).reprompt(re_message)

@ask.intent("SearchIntent")
def search_intent(query):
	return statement(query)
	
@ask.intent('AMAZON.CancelIntent')
@ask.intent('AMAZON.StopIntent')
def stop_alexa():
    quit = "Goodbye then."
    return statement(quit)

if __name__ == '__main__':
	app.run(debug=True)
