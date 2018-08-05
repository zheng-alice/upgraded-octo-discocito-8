from flask import Flask
from flask_ask import Ask, statement

app = Flask(__name__)
ask = Ask(app, '/')

from poem_gen import genHappy
@ask.launch
def start_skill():
    return statement(genHappy())

if __name__ == '__main__':
    app.run(debug = True)