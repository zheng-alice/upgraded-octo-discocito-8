from flask import Flask
from flask_ask import Ask, statement, question
import requests
import time
import unidecode
import json
import random

import numpy as np
from collections import Counter
from collections import defaultdict
import pickle

app = Flask(__name__)
ask = Ask(app, '/')

@app.route('/')
def homepage():
    return "Hello"

@ask.launch
def start():
    original = "Do you want to hear a joke?"
    re = "I didn't catch that. Do you want to hear a joke?"
    return question(original).reprompt(re)

def normalize(counter):
    """ Converts a letter -> count counter to a list of (letter, 
    frequency) pairs, sorted in descending order of frequency.
    
        Parameters
        -----------
        counter : collections.Counter
            letter -> count
            
        Returns
        -------
        A list of (letter, frequency) pairs, sorted in descending 
        order of frequency. """

    total = sum(counter.values())
    return [(char, cnt/total) for char, cnt in counter.most_common()]
    
def train_lm(text, n):
    """ Trains a character-based n-gram language model.
        
        Parameters
        -----------
        text: str 
            
        n: int
            the length of the n-gram to analyze.
        
        Returns
        -------
        A dictionary that maps history to a list of tuples that 
        describes the probability of each following character. """
    
    raw_lm = defaultdict(Counter)
    # padding
    history = "~" * (n - 1)
    
    for char in text:
        raw_lm[history][char] += 1
        history = history[1:] + char
    
    lm = {history : normalize(counter) for history, counter in raw_lm.items()}
    return lm
        
def generate_letter(lm, history):
    """ Randomly generates a letter according to the probability 
    distribution associated with the specified history.
        
        Parameters
        ----------
        lm: Dict[str, List[Tuple[str, float]]] 
            the n-gram language model. 
        
        history: str
            a string of length (n-1) to use as history when generating 
            the next character.
        
        Returns
        -------
        A tuple containing the predicted character and the history. """
    
    if not history in lm:
        if history[-1] == '\n':
            return ('A', history)
        elif history[-1] == 'A':
            return (':', history)
        elif history[-1] == ':':
            return (' ', history)
        else:
        	# forcibly change history
            A_list = [hist for hist in lm.keys() if hist.endswith('\nA: ')]
            A_i = np.random.randint(len(A_list))
            history = A_list[A_i]
    letters, probs = tuple(zip(*lm[history]))
    i = np.random.choice(letters, p=probs)
    return (i, history)
        
def generate_text(lm, n, nletters = 200):
    """ Randomly generates text by drawing from the probability 
    distributions stored in the n-gram language model.
    
        Parameters
        ----------
        lm: Dict[str, List[Tuple[str, float]]]
            the n-gram language model. 
            
        n: int
            order of n-gram model.
            
        nletters: int
            number of letters to randomly generate.
        
        Returns
        -------
        Model-generated text. """
    
    history = '~' * (n - 1)
    text = []
    finished = False
    for i in range(nletters):
        # keeps joke in Q&A format
        if history[-1] == '\n':
            c = 'A'
            finished = True
        else:
            c, history = generate_letter(lm, history)
        if finished and c == '\n':
            break
        text.append(c)
        history = history[1:] + c
    return "".join(text)
    
@ask.intent("AMAZON.YesIntent")
def gen_joke():
    with open("lm_jokes.pkl", mode="rb") as f:
        lm_jokes = pickle.load(f)
    
    joke = generate_text(lm_jokes, 8)
    joke = joke.replace('Q: ', '')
    joke = joke.replace('A: ', '<break time="0.5s"/>')
    joke = "<speak>" + joke + "</speak>"

    return statement(joke)

@ask.intent("AMAZON.FallbackIntent")
def no_ans():
    return question("I'm sorry, but I didn't catch that. Do you want to hear a joke?")            	

@ask.intent('AMAZON.CancelIntent')
@ask.intent('AMAZON.StopIntent')
@ask.intent('AMAZON.NoIntent')
def stop_alexa():
    quit = "Goodbye then."
    return statement(quit)

if __name__ == '__main__':
	app.run(debug=True)
