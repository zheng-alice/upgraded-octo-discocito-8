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
import string

app = Flask(__name__)
ask = Ask(app, '/')

@app.route('/')
def homepage():
    return "Hello"

@ask.launch
def start():
    original = "Do you want to hear a joke?"
    return question(original)

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
    history = text[:n]
    
    for char in text[n:]:
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
        # returns a random letter
        return chr(np.random.randint(97, 97 + 26))
    letters, probs = tuple(zip(*lm[history]))
    i = np.random.choice(letters, p=probs)
    return i

def generate_phrase(lm, n, total_words = 1):
    """ Randomly generates a phrase by drawing from the probability 
    distributions stored in the n-gram language model.
    
        Parameters
        ----------
        lm: Dict[str, List[Tuple[str, float]]]
            the n-gram language model. 
            
        n: int
            order of n-gram model.
            
        total_words : int
            the number of words to be generated
        
        Returns
        -------
        Model-generated phrase. """
    
    # chooses a random word to start with as history
    word_start_hist = [hist[1:] for hist in lm.keys() if hist.startswith(' ')]
    i = np.random.randint(len(word_start_hist))
    history = word_start_hist[i]
    
    text = []
    text.extend(history)
    
    spaces = 0
    
    while True:
        c = generate_letter(lm, history)
        # counts number of words
        if c == ' ':
            spaces += 1
            if spaces == total_words:
                break
        text.append(c)
        history = history[1:] + c
        
    return "".join(text)

@ask.intent("YesIntent")
def n_gram_jokes():
    """ Generates a really funny joke based on a text file of words.
                                    
        Returns
        -------
        A really funny joke. """

    n = 5
    path_to_nouns = "nouns.txt"
    path_to_verbs = "verbs.txt"

    with open(path_to_nouns, "r") as f:
        nouns = f.read()
    nouns = " ".join(nouns.split())
    
    with open(path_to_verbs, "r") as f:
        verbs = f.read()
    verbs = " ".join(verbs.split())
    
    lm_noun = train_lm(nouns, n)
    lm_verb = train_lm(verbs, n)
        
    jokes = ["Knock knock. \nWho's there? \n{0} \n{0} who? \n{0} {1} ".format(generate_phrase(lm_noun, n, np.random.randint(1, 3)).capitalize(), generate_phrase(lm_noun, n, np.random.randint(1, 3))),                
             "Why did the {} {} the {}? \nTo {} {}!".format(generate_phrase(lm_noun, n, np.random.randint(1, 3)), generate_phrase(lm_verb, n), generate_phrase(lm_noun, n, np.random.randint(1, 3)), generate_phrase(lm_verb, n), generate_phrase(lm_noun, n, np.random.randint(1, 3))),
             "*slaps roof of {0}* \nThis {0} can fit so much {1} in it".format(generate_phrase(lm_noun, n), generate_phrase(lm_noun, n)),
             "Thank you {} very {}".format(generate_phrase(lm_noun, n, np.random.randint(1, 3)), generate_phrase(lm_noun, n, np.random.randint(1, 3)))]    
    i = np.random.randint(len(jokes))    
    return statement(jokes[i])
	
@ask.intent('AMAZON.CancelIntent')
@ask.intent('AMAZON.StopIntent')
@ask.intent('AMAZON.NoIntent')
def stop_alexa():
    quit = "Goodbye then."
    return statement(quit)

if __name__ == '__main__':
	app.run(debug=True)
