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
def start_skill():
    welcome_message = 'Hello there, would you like to hear a compliment?'
    ree = "Sorry I missed that. Would you like to hear a compliment?"
    return question(welcome_message)

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
    # no padding characters so that generated text starts with different letter combinations
    history = text[:n - 1]
    
    for char in text[n - 1:]:
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
        The predicted character. """
    
    if not history in lm:
        # ends sentence
        return '\n'
    letters, probs = tuple(zip(*lm[history]))
    i = np.random.choice(letters, p=probs)
    return i

def generate_sentence(lm, n):
    """ Randomly generates a sentence by drawing from the probability 
    distributions stored in the n-gram language model.
    
        Parameters
        ----------
        lm: Dict[str, List[Tuple[str, float]]]
            the n-gram language model. 
            
        n: int
            order of n-gram model.
            
        Returns
        -------
        Model-generated sentence. """
    
    # chooses a random sentence starter to start with as history
    word_start_hist = [hist for hist in lm.keys() if hist.startswith('\n')]
    i = np.random.randint(len(word_start_hist))
    history = word_start_hist[i]
    
    sentence = []
    sentence.extend(history[1:])
    
    spaces = 0
    
    while True:
        c = generate_letter(lm, history)
        if c == '\n':
            break
        sentence.append(c)
        history = history[1:] + c
        
    out = "".join(sentence)
    return out[0].capitalize() + out[1:]

@ask.intent("AMAZON.YesIntent")
def gen_compliment():
    with open("lm_comps.pkl", mode="rb") as f:
        lm = pickle.load(f)
        
    return statement(generate_sentence(lm, 8))

@ask.intent("AMAZON.NoIntent")
def no_intent():
    bye_text = 'Okay, goodbye'
    return statement(bye_text)

@ask.intent("AMAZON.FallbackIntent")
def nope():
    return question("I'm sorry, I missed that. Would you like to hear a compliment?")

if __name__ == '__main__':
    app.run(debug=True)
    

