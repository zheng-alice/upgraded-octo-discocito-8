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

app = Flask(__name__)
ask = Ask(app, '/')

@app.route('/')
def homepage():
    return "Hello"

@ask.intent("YesIntent")
def gen_assurance():
    return question("Let's chat.")

@ask.intent("NoIntent")
def no_intent():
    bye_text = 'Okay, goodbye'
    return statement(bye_text)

@ask.launch
def start_skill():
    welcome_message = 'Hello there, I heard you were going through a tough time. Would you like to chat?'
    ree = "Sorry I missed that. Would you like me to talk to me?"
    return question(welcome_message).reprompt(ree)

@ask.intent("AMAZON.FallbackIntent")
def nope():
    with open("assurance.txt", "rb") as f:
        console = f.read().decode()
    a = console.split('\n') 
    ran = np.random.randint(0,high=len(a))
    return question(a[ran])

if __name__ == '__main__':
    app.run(debug=True)
    

    