import logging
import os
import threading
import numpy as np

from flask import Flask, json, render_template
from flask_ask import Ask, request, session, question, statement, context, audio, current_stream

app = Flask(__name__)
ask = Ask(app, "/")
logger = logging.getLogger()
logging.getLogger('flask_ask').setLevel(logging.INFO)


@ask.launch
def launch():
    card_title = 'DESPACITO TIME'
    text = 'Hey there. Are you ready?'
    prompt = 'Are you ready?'
    return question(text).reprompt(prompt).simple_card(card_title, text)

@ask.intent('YesIntent')
def demo():
    speech = ("You got it bud!",
        "Let's get this party started",
        "Let's go amigos!",
        "Get ready for a good time!",
        "Awesome, I love this song!",
        "I'm so excited!",
        "You got it buddy")
    stream_url = 'https://ia601500.us.archive.org/34/items/DESPACITOBASSBOOSTEDdespacito2/DESPACITO%20-%20BASS%20BOOSTED%20%28despacito%202%29.mp3'
    return audio(speech[np.random.randint(0,len(speech))]).play(stream_url, offset=0)

@ask.intent("AMAZON.FallbackIntent")
def no_query():
    return statement("Sorry I didn't catch that. If you are feeling sad and want to play despacito, then say Alexa despacito")


# 'ask audio_skil Play the sax
@ask.intent('NoIntent')
def no_intent():
    bye_text = 'Well then, youre missing out!'
    return statement(bye_text)


@ask.intent('AMAZON.PauseIntent')
def pause():
    return audio('Paused the lit musica.').stop()


@ask.intent('AMAZON.ResumeIntent')
def resume():
    return audio('Resuming.').resume()

@ask.intent('AMAZON.StopIntent')
def stop():
    return audio('stopping').clear_queue(stop=True)



# optional callbacks
@ask.on_playback_started()
def started(offset, token):
    _infodump('STARTED Audio Stream at {} ms'.format(offset))
    _infodump('Stream holds the token {}'.format(token))
    _infodump('STARTED Audio stream from {}'.format(current_stream.url))


@ask.on_playback_stopped()
def stopped(offset, token):
    _infodump('STOPPED Audio Stream at {} ms'.format(offset))
    _infodump('Stream holds the token {}'.format(token))
    _infodump('Stream stopped playing from {}'.format(current_stream.url))


@ask.on_playback_nearly_finished()
def nearly_finished():
    _infodump('Stream nearly finished from {}'.format(current_stream.url))

@ask.on_playback_finished()
def stream_finished(token):
    _infodump('Playback has finished for stream with token {}'.format(token))

@ask.session_ended
def session_ended():
    return "{}", 200

def _infodump(obj, indent=2):
    msg = json.dumps(obj, indent=indent)
    logger.info(msg)


if __name__ == '__main__':
    if 'ASK_VERIFY_REQUESTS' in os.environ:
        verify = str(os.environ.get('ASK_VERIFY_REQUESTS', '')).lower()
        if verify == 'false':
            app.config['ASK_VERIFY_REQUESTS'] = False
    app.run(debug=True)
