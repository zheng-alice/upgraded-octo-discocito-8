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
    card_title = 'Time to Meditate'
    text = 'Welcome. Would you like to begin, and what kind of meditation would you like? Ocean, classical music, rain, or guided?'
    prompt = 'Would you like to begin, and what kind of meditation would you like? Ocean, classical music, rain, or guided?'
    return question(text).reprompt(prompt).simple_card(card_title, text)


@ask.intent('YesIntent')
def demo(sound_type):
    #speech = "Ok, let's begin. Close your eyes and embrace the zen."
    #return audio(sound_type)

    guided_meds = ['https://ia800304.us.archive.org/24/items/HealthyLivingGuidedMeditation/HealthJourneys-GeneralWellness-02Of2.mp3',
        'https://ia800304.us.archive.org/24/items/HealthyLivingGuidedMeditation/HealthJourneys-GeneralWellness-01Of2.mp3',
        'https://ia800304.us.archive.org/4/items/BasicGuidedMeditation/GuidedMeditation.mp3',
        'https://ia800200.us.archive.org/20/items/GuidedMeditation2015/Guided_Meditation_16_2016-02-28.mp3',
        'https://ia800205.us.archive.org/12/items/RamakrishnaMissionGuidedMeditation/02_Guided_Meditation.mp3']

    if sound_type == "classical music" or sound_type == "classical":
        speech = "Alright, let's begin. Close your eyes and embrace the classical zen."
        stream_url = 'https://ia800102.us.archive.org/2/items/ClassicalMusicWithOceanWavesAndNatureSoundsRelaxingMusic_201711/Classical%20Music%20with%20Ocean%20Waves%20and%20Nature%20Sounds%20%28Relaxing%20Music%29.mp3'
    elif sound_type == "rain" or sound_type == "rain sounds":
        speech = "Alright, let's begin. Close your eyes and embrace the rain zen."
        stream_url = 'https://ia800803.us.archive.org/24/items/RainSounds10HoursTheSoundOfRainMeditationAutogencTrainingDeepSleepRelaxingSounds/Rain%20Sounds%2010%20HoursThe%20Sound%20of%20Rain%20MeditationAutogenc%20Training%20Deep%20SleepRelaxing%20Sounds.mp3'
    elif sound_type == "ocean" or sound_type == "ocean sounds":
        speech = "Alright, let's begin. Close your eyes and embrace the ocean zen."
        stream_url = 'https://ia800408.us.archive.org/31/items/ocean-sea-sounds/Those_Relaxing_Sounds_of_Waves_-_Ocean_Sounds_1080p_HD_Video_with_Tropical_Beaches%20Part%202.mp3'
    elif sound_type == "guided meditation" or sound_type == "guided":
        speech = "Alright, let's begin. Close your eyes and embrace the zen."
        stream_url = guided_meds[np.random.randint(0,len(guided_meds))]
    else: 
        speech = "I didn't catch that. Why don't we just go with ocean sounds."
        stream_url = 'https://ia800408.us.archive.org/31/items/ocean-sea-sounds/Those_Relaxing_Sounds_of_Waves_-_Ocean_Sounds_1080p_HD_Video_with_Tropical_Beaches%20Part%202.mp3'

    return audio(speech).play(stream_url, offset=93000)

@ask.intent("AMAZON.FallbackIntent")
def no_query():
    return statement("Sorry I didn't get that. If you would like to meditate with me, say 'yes', and then the preferred background music, choosing between ocean, classical, and rain.")


# 'ask audio_skil Play the sax
@ask.intent('NoIntent')
def no_intent():
    bye_text = 'Okay, goodbye'
    return statement(bye_text)


@ask.intent('AMAZON.PauseIntent')
def pause():
    return audio('Paused the meditation.').stop()


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
