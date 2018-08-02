import numpy as np
import re
from nltk.corpus import stopwords

stops = set(stopwords.words("english"))

at_sub = re.compile(r'@.*?(?=\s)')
whitespace_sub = re.compile(r'[^\w\s ]')
space_sub = re.compile(' +')
non_alpha_numeric = re.compile('[^a-zA-Z0-9-_.]')


def new_preprocess(path):
    """ Given path to twitter npz file, return list of tuples. Each
        tuple contains the preprocessed words (a.k.a tokens) for a
        single tweet. Also returned is the token-length of the longest
        preprocessed twee

        Parameters
        ----------
        path : PathLike

        Returns
        --------
        List[Tuple[str, ...], ...], int
            The list of tuples-of-tokens. One tuple for each tweet.
            And the length of the longest tweet
        """

    with np.load(path) as f:
        array_of_sent = f["arr_0"]

    max_sent_len = 0
    out_data = []
    for sent in array_of_sent:
        sent = sent.item()
        sent = sent.lstrip()
        sent = re.sub(r'@.*?(?=\s)', '', sent)
        sent = at_sub.sub("", sent)
        sent = sent.replace("&quot;", "")
        sent = whitespace_sub.sub("", sent)
        sent = space_sub.sub(" ", sent)

        sent = sent.split()
        sent = tuple(non_alpha_numeric.sub('', word).lower() for word in sent if word not in stops)
        if len(sent) > max_sent_len:
            max_sent_len = len(sent)
        out_data.append(sent)

    return out_data, max_sent_len



def preprocess():
    x_test = np.load('./data/test_twitter_data.npz')
    x_test = x_test.f.arr_0
    x_train = np.load('./data/train_twitter_data.npz')
    x_train = x_train.f.arr_0
    MAX = 0
    for sent in x_test:
        sent[0] = sent[0].lstrip()
        sent[0] = re.sub(r'@.*?(?=\s)', '', sent[0])
        sent[0] = sent[0].replace("&quot;", "")
        sent[0] = re.sub(r'[^\w\s ]','',sent[0])
        sent[0] = re.sub(' +',' ',sent[0])
        sent[0] = sent[0].split()
        stops = set(stopwords.words("english"))
        sent[0] = [word for word in sent[0] if word not in stops]
        for count, word in enumerate(sent[0]):
            word = re.sub('[^a-zA-Z0-9-_.]', '', word)
            word = word.lower()
            if count > MAX:
                MAX = count

    for sent in x_train:
        sent[0] = sent[0].lstrip()
        sent[0] = re.sub(r'@.*?(?=\s)', '', sent[0])
        sent[0] = sent[0].replace("&quot;", "")
        sent[0] = re.sub(r'[^\w\s ]','',sent[0])
        sent[0] = re.sub(' +',' ',sent[0])
        sent[0] = sent[0].split()
        stops = set(stopwords.words("english"))
        sent[0] = [word for word in sent[0] if word not in stops]
        for count, word in enumerate(sent[0]):
            word = re.sub('[^a-zA-Z0-9-_.]', '', word)
            word = word.lower()
            if count > MAX:
                MAX = count
    MAX += 1 #cuz enumerate is stupid       
    for i in x_train:
        for j in range(len(i[0]), MAX):
            i[0] = np.append(i[0], 0)
    for i in x_test:
        for j in range(len(i[0]), MAX):
            i[0] = np.append(i[0], 0)
    x_train = np.concatenate( x_train.flatten().tolist(), axis=0 ).reshape(len(x_train.flatten().tolist()), -1)
    x_test = np.concatenate( x_test.flatten().tolist(), axis=0 ).reshape(len(x_test.flatten().tolist()), -1)
    np.save('./data/x_train_text', x_train)
    np.save('./data/x_test_text', x_test)
    y_train = np.load('./data/train_twitter_label.npz')
    y_test = np.load('./data/test_twitter_label.npz')
    y_train = y_train.f.arr_0.astype(int)
    y_test = y_test.f.arr_0.astype(int)
    return (x_train, y_train, x_test, y_test)