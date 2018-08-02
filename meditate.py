import numpy as np
#%matplotlib notebook
#import matplotlib.pyplot as plt

from flask import Flask
from flask_ask import Ask, statement, question
import requests
import time
import unidecode
import json
import random
import librosa

app = Flask(__name__)
ask = Ask(app, '/')

@app.route('/')
def homepage():
    return "Hello"

@ask.intent("YesIntent")
def gen_assurance():
	local_song_path = "1_Hour_Relaxing_Ocean_Waves.mp3"
	samples, fs = librosa.load(local_song_path, sr=44100, mono=True, duration=11)
	arr = np.array_str(samples)
	arr = arr.copy()
	return statement(len(arr))
    
@ask.intent("NoIntent")
def no_intent():
    bye_text = 'Okay, goodbye'
    return statement(bye_text)

@ask.launch
def start_skill():
    welcome_message = 'Hello there, would you like to meditate?'
    return question(welcome_message)

if __name__ == '__main__':
    app.run(debug=True)
    

    