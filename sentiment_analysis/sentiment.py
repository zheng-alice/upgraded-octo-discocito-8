from gensim.models.keyedvectors import KeyedVectors
import torch
from pickle import load

path = "glove.6B.50d.txt.w2v"
glove = KeyedVectors.load_word2vec_format(path, binary=False)

def process(tweets):
    '''
    Takes in a batch of tweets and formats them for training.
    
    INPUT:
        tweets - batch of tweets to process.
        
    OUTPUT:
        ret - processed tweets as word embeddings ready for the RNN.
    '''
    ret = torch.zeros((len(tweets), len(max(tweets, key = len)), 50))
    for n in range(len(tweets)):
        tweet = tweets[n]
        for x in range(len(tweet)):
            word = tweet[x]
            if word in glove:
                ret[n, x] = torch.tensor(glove[word])
    return ret

def sentiment(sentence, path = 'sentnet.dat'):
    '''
    Decides whether or not a string has happy sentiment.
    
    INPUTS:
        sentence - string to be analyzed
        path (optional) - string with the path to the databse
        
    OUTPUT:
        sentiment (int) - 0 if the sentiment is negative, 1 if it's positive.
    '''
    net = load(open(path, 'rb'))
    sentence = process([sentence.split()])
    sentence = torch.transpose(sentence, 1, 2)
    return torch.argmax(net(sentence)).item()

import torch.nn as nn
import torch.nn.functional as F

class Model(nn.Module):
    
    def __init__(self, dim_input = 50, dim_recurrent = 100, dim_output = 2):
        
        '''
        Initializes the model.
        
        INPUTS:
            dim_input - The dimensionality of the input data.
                Defaults to 50, the size of word embeddings.
            dim_recurrent - The number of recurrent layers.
                This is a hyperparameter. Defaults to 100.
            dim_output - The number of predictions to make.
                Defaults to 2, the number of predictions the model should make.
                
        OUTPUTS:
            None
        '''
        #Initializes model as a pytorch object
        super(Model, self).__init__()
        
        #Initializes internal variables
        self.C = dim_input
        self.D = dim_recurrent
        self.K = dim_output
        
        
        #Initializes the internal layers of the network.
        self.dense1 = nn.Linear(dim_input, dim_recurrent)
        self.dense2 = nn.Linear(dim_recurrent, dim_recurrent, bias = False)
        self.dense3 = nn.Linear(dim_input, dim_recurrent)
        self.dense4 = nn.Linear(dim_recurrent, dim_recurrent, bias = False)
        self.dense5 = nn.Linear(dim_recurrent, dim_output)
        
    def forward(self, x):
        
        '''
        Takes in a batch of N tweets and outputs N predictions from an RNN.
        
        INPUT:
            x - batch of tweets to be processed.
            
        OUTPUT:
            predictions - predictions for each tweet.
        
        '''
        
        #Creates the hidden layer
        hidden = torch.zeros(len(x), self.D)
        
        #Processes each row
        for i in range(x.shape[2]):
            row = x[:, :, i]
            
            #Iterates through the RNN
            subHid = self.dense1(row)
            mem = self.dense2(hidden)
            subHid += mem
            subHid = F.relu(subHid)
            z = F.sigmoid(self.dense3(row) + self.dense4(hidden))
            hidden = z * hidden + (1 - z) * subHid
        
        #Converts the final hidden state to predictions.
        return self.dense5(hidden)