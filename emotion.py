from flask import Flask
from flask_ask import Ask, statement, question, session
import requests
import time
import unidecode
import json
import random

from sentiment_analysis.sentiment import *
import face_recognizer.final as face
from camera import take_picture
import numpy as np
import pickle

app = Flask(__name__)
ask = Ask(app, '/')

@app.route('/')
def homepage():
    return "Hello"

@ask.launch
def record_voice():
	intro1 = ["Hi. ",
	"Hi there. ",
	"Hello. ",
	"Hello there. ",
	"Hey. ",
	"Hey there. ",
	"Hi buddy. ",
	"Hi pal. ",
	"Hey yo. "]

	intro2 = ["I'm Peanuts. ",
	"I'm Peanuts, your personalized emotional assistant. ",
	"I'm Peanuts, your personalized emotional assistant: nice, understanding, trustworthy, sincere. ",
	"My name is Peanuts. ",
	"My name is Peanuts. I'm your personalized emotional assistant. ",
	"My name is Peanuts. I'm your personalized emotional assistant: nice, understanding, trustworthy, sincere. ",
	"My name is Peanuts, your personalized emotional assistant. ",
	"Call me Peanuts. ",
	"Call me Peanuts, your personalized emotional assistant. ",
	"Call me Peanuts, your personalized emotional assistant: nice, understanding, trustworthy, sincere. "]

	intro3 = ["How was your day?",
	"What's up?",
	"How's it going?",
	"How have you been?",
	"How do you feel?",
	"What's crackalackin?",
	"How do you do?", 
	"What's popping?",
	"How are you doing?"]

	intro = intro1[np.random.randint(len(intro1))] + intro2[np.random.randint(len(intro2))] + intro3[np.random.randint(len(intro3))]
	re_message = "I'm sorry, but I didn't understand that. Try again, this time prefacing your statement with my name, Peanuts."
	return question(intro).reprompt(re_message)

@ask.intent("SearchIntent")
def search_intent(query):
	with open("stats.pkl", mode="rb") as f:
		stats = pickle.load(f)

	voice_sent = sentiment(query, path = 'sentiment_analysis/sentnet.dat')

	img = take_picture()
	img = img.copy(order='C')
	img = np.array(img)
	face_sent_str = face.faceRec2('/Users/christinaxiao/Christina/COLLEGE/Camps/MIT BWSI/Class/Week 2 - Visual/upgraded-octo-discocito-3/dataface/dataface.dat', img)
	
	if face_sent_str == 'sad':
		face_sent = 0
	elif face_sent_str == 'neutral':
		face_sent = 0.5
	else:
		face_sent = 1

	sent = round(.5 * voice_sent + .5 * face_sent)

	stats[sent] += 1
	with open("stats.pkl", mode="wb") as f:
		pickle.dump(stats, f)

    # sad
	if sent == 0:
		sad = ["I'm sorry to hear that. ",
		"Oh no, I'm sorry to hear that. ",
		"I sorry to hear you’re having a hard time. ",
		"Oh no. "]

		# very sad
		if stats[0] + stats[1] >= 5 and stats[0] / (stats[0] + stats[1]) >= 0.8:
			recs = ["You seem to be really sad lately. I recommend you talk to me by saying 'Alexa let's talk,' or meditate with me by saying 'Alexa let's meditate.'",
			"You seem to be really sad lately. I think you should talk to me by saying 'Alexa let's talk,' or meditate with me by saying 'Alexa let's meditate.'",
			"You seem to be really sad lately. Try talking to me by saying 'Alexa let's talk,' or meditating with me by saying 'Alexa let's meditate.'",
			"You seem to be really sad lately. Why don't you talk to me by saying 'Alexa let's talk,' or meditate with me by saying 'Alexa let's meditate?'"]
		# kinda sad
		else: 
			recs = ["I recommend you meditate with me by saying 'Alexa let's meditate,' or listen to a short story by saying 'Alexa sad story.' If you want me to cheer you up, you can also say 'Alexa Despacito time' to play Despacito, or 'Alexa jokebot' to listen to one of my jokes.",
			"I think you should meditate with me by saying 'Alexa let's meditate,' or listen to a short story by saying 'Alexa sad story.' If you want me to cheer you up, you can also say 'Alexa Despacito time' to play Despacito, or 'Alexa jokebot' to listen to one of my jokes.",
			"Try meditating with me by saying 'Alexa let's meditate,' or listening to a short story by saying 'Alexa sad story.'' If you want me to cheer you up, you can also say 'Alexa Despacito time' to play Despacito, or 'Alexa jokebot' to listen to one of my jokes.",
			"Why don't you meditate with me by saying 'Alexa let's meditate,' or listen to a short story by saying 'Alexa sad story.'? If you want me to cheer you up, you can also say 'Alexa Despacito time' to play Despacito, or 'Alexa jokebot' to listen to one of my jokes."]

		return statement(sad[np.random.randint(len(sad))] + recs[np.random.randint(len(recs))])
	# happy
	else:
		happy = ["That's great! ",
		"I'm so happy for you! ",
		"I'm glad you're doing well. ",
		"Sounds exciting! ",
		"Sounds great! ",
		"Cool! "]

		recs = ["I think you should listen to a joke by saying 'Alexa jokebot,' a meme by saying 'Alexa memebot,' or a short story by saying, 'Alexa happy story.' I can also compliment you if you say 'Alexa compliment me'!",
		"Try listening to a joke by saying 'Alexa jokebot,' a meme by saying 'Alexa memebot,' or a short story by saying, 'Alexa happy story.' I can also compliment you if you say 'Alexa compliment me'!",
		"Why don't you listen to a joke by saying 'Alexa jokebot,' a meme by saying 'Alexa memebot,' or a short story by saying, 'Alexa happy story.'? I can also compliment you if you say 'Alexa compliment me'!"]

		return statement(happy[np.random.randint(len(happy))] + recs[np.random.randint(len(recs))])
	
@ask.intent("AMAZON.FallbackIntent")
def no_query():
	return question("I'm sorry, but I didn't understand that. Try again, this time prefacing your statement with my name, Peanuts.")
	
@ask.intent('AMAZON.CancelIntent')
@ask.intent('AMAZON.StopIntent')
def stop_alexa():
    quit = "Goodbye then."
    return statement(quit)

if __name__ == '__main__':
	app.run(debug=True)