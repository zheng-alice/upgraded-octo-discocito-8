from pickle import load
import numpy as np

with open('happy.dat', 'rb') as f:
    happy_lm = load(f)
    
with open('sad.dat', 'rb') as f:
    sad_lm = load(f)

def unzip(pairs):
    """
    "unzips" of groups of items into separate lists.
    
    Example: pairs = [("a", 1), ("b", 2), ...] --> (("a", "b", ...), (1, 2, ...))
    """
    return tuple(zip(*pairs))

def generate_letter(lm, history):
    """ Randomly picks letter according to probability distribution associated with 
        the specified history, as stored in your language model.
    
        Note: returns dummy character "~" if history not found in model.
    
        Parameters
        ----------
        lm: Dict[str, List[Tuple[str, float]]] 
            The n-gram language model. 
            I.e. the dictionary: history -> [(char, freq), ...]
        
        history: str
            A string of length (n-1) to use as context/history for generating 
            the next character.
        
        Returns
        -------
        str
            The predicted character. '~' if history is not in language model.
    """
    if not history in lm:
        return "~"
    letters, probs = unzip(lm[history])
    i = np.random.choice(letters, p=probs)
    return i

def generate_text(lm, n, nletters=100):
    """ Randomly generates `nletters` of text by drawing from 
        the probability distributions stored in a n-gram language model 
        `lm`.
    
        Parameters
        ----------
        lm: Dict[str, List[Tuple[str, float]]]
            The n-gram language model. 
            I.e. the dictionary: history -> [(char, freq), ...]
        n: int
            Order of n-gram model.
        nletters: int
            Number of letters to randomly generate.
        
        Returns
        -------
        str
            Model-generated text.
    """
    history = "~" * (n - 1)
    text = []
    for i in range(nletters):
        c = generate_letter(lm, history)
        text.append(c)
        history = history[1:] + c
    return "".join(text)    

def genHappy(letters = 500, N = 13):
    text = generate_text(happy_lm, N, letters)
    if '.' in text:
        while text[-1] != '.':
            text = text[:-1]
    return text

def genSad(letters = 500, N = 13):
    text = generate_text(sad_lm, N, letters)
    if '.' in text:
        while text[-1] != '.':
            text = text[:-1]
    return text 