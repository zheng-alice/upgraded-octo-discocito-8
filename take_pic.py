from camera import take_picture
from flask import Flask
from flask_ask import Ask, statement, question
import requests
import time
import unidecode
import json
import random
import numpy as np

app = Flask(__name__)
ask = Ask(app, '/')

@app.route('/')
def homepage():
    return "Hello"

@ask.intent("YesIntent")
def camera_to_image_array():
    """ Takes a picture and loads it as an image array.
                            
        Returns
        -------
        The picture as an image array. """    
    img = take_picture()
    img = img.copy(order='C')
    img = np.array_str(img)
    #img = img.encode()
    return statement(img)

@ask.intent("NoIntent")
def no_intent():
    bye_text = 'Okay, goodbye'
    return statement(bye_text)


@ask.launch
def start_skill():
    welcome_message = 'Hello there, would you like me to detect the emotion on your face?'
    return question(welcome_message)

if __name__ == '__main__':
    app.run(debug=True)

'''
import random

#note how this function does NOT start with @ask.intent() because it is not an intent and does not interact
#directly with the alexa app.
def flip_coin():
    #randomly generate either 0 or 1
    c = random.randint(0, 1)
    if c == 0:
        return "heads"
    else:
        return "tails"
'''