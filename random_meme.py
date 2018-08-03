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
    original = "Do you want to hear a meme?"
    re_mess = "I didn't catch that. Do you want to hear a meme?"
    return question(original).reprompt(re_mess)

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
    
    # chooses a random word to start with as history
    word_start_hist = [hist for hist in lm.keys() if hist.startswith(' ')]
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
    
def choose(*choices):
    i = np.random.randint(len(choices))
    return choices[i]

def rand(l):
    return l[np.random.randint(len(l))]

@ask.intent("AMAZON.YesIntent")
def generate_meme():
    with open("nouns.txt", "r") as f:
        nouns = f.read()
    nouns = list(set(nouns.split()))

    with open("verbs.txt", "r") as f:
        verbs = f.read()
    verbs = list(set(verbs.split()))

    with open("adjs.txt", "r") as f:
        adjs = f.read()
    adjs = list(set(adjs.split()))
    
    with open("names.txt", "r") as f:
        names = f.read()
    names = list(set(names.split('\n')))
    
    with open("sents.pkl", "rb") as f:
        lm = pickle.load(f)
                
    jokes = ["*slaps roof of {0}*. \nThis {0} can fit so much {1} {2} in it.".format(rand(nouns), rand(adjs), rand(nouns)),
             "Thank you {} very {}.".format(rand(names), rand(adjs)),
             "This is so {} Alexa play {}.".format(rand(adjs), choose(rand(nouns).capitalize(), rand(adjs).capitalize(), rand(verbs).capitalize(), rand(adjs).capitalize() + ' ' + rand(nouns).capitalize())),
             "Dad, why is my sister's name {0} {1}? \nBecause your mother loves {0} {1}. \nThanks Dad. \nNo problem {2}.".format(rand(adjs).capitalize(), rand(nouns).capitalize(), rand(nouns).capitalize()),
             "{} announces {} {}. \n{} rate drops to 0%.".format(choose(rand(nouns).capitalize(), rand(names)), rand(nouns).capitalize(), str(np.random.randint(1, 11)), rand(nouns).capitalize()),
             "{} are now statistically more popular than {}.".format((rand(nouns) + 's').capitalize(), rand(nouns) + 's'),
             "You can't {0} a {1} if you don't {2} a {1}.".format(rand(verbs), rand(nouns), rand(verbs)),
             "Little known fact: \n{} was invented in {} by {} when he tried to {} twice at the same time.".format(choose(rand(verbs).capitalize() + 'ing', rand(nouns).capitalize()), str(np.random.randint(1200, 2019)), rand(names), rand(verbs)),
             "{} is just {}. \nChange my mind.".format(choose((rand(verbs) + 'ing').capitalize(), rand(nouns).capitalize()), choose(rand(verbs) + 'ing', rand(nouns), rand(adjs))),
             "@Google {} \nDad: Why is the FBI here?".format(generate_sentence(lm, 7)),
             "{} {} is the most ambitious crossover event in history.".format(rand(adjs).capitalize(), rand(nouns).capitalize()),
             'When {} said "{}," I felt that.'.format(rand(names), choose(rand(adjs) + ' ' + rand(nouns), rand(nouns) + 's ' + rand(verbs), rand(adjs) + ' ' + rand(nouns) + 's ' + rand(verbs), generate_sentence(lm, 7))),
             "You: {} \nMe, an intellectual: {}".format(generate_sentence(lm, 7), generate_sentence(lm, 7)),
             "Petition: Make {} {}. 6,953 have signed. Let's get to 7,500!".format(rand(nouns) + 's', rand(verbs)),
             "Is it normal to {} your {}? \n{} wants to know your location.".format(rand(verbs), rand(nouns), rand(names)),
             "Who would win? \n{} {}. \nOne {} boi.".format(str(np.random.randint(1000, 10000)), rand(nouns) + 's', rand(adjs)),
             "You wouldn't {} a {}.".format(rand(verbs), rand(nouns)),
             "Her: He's probably thinking about other girls. \nHim: {}".format(generate_sentence(lm, 7)),
             "{} \n-{}".format(generate_sentence(lm, 7), rand(names))]
    i = np.random.randint(len(jokes))    
    return statement(jokes[i])
            	
@ask.intent("AMAZON.FallbackIntent")
def no_ans():
    return question("I'm sorry, but I didn't catch that. Do you want to hear a meme?")

@ask.intent('AMAZON.CancelIntent')
@ask.intent('AMAZON.StopIntent')
@ask.intent('AMAZON.NoIntent')
def stop_alexa():
    quit = "Goodbye then."
    return statement(quit)

if __name__ == '__main__':
	app.run(debug=True)
