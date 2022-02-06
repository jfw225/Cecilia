from Cecilia import Cecilia
import speech_recognition as sr
import os
import time
from queue import Queue
from threading import Thread
from spotipy import SpotifyException


def listen(args):
    ceci, input_q = args
    r = sr.Recognizer()
    mic = ceci.get_mic()
    phrase_time_limit = 20

    ceci.play_sound('Hello, Joseph.')
    ceci.plog("Ready to listen...")
    with mic as source:
        while True:
            try:
                with ceci._speak_lock:
                    listen_time = time.time()
                    text = r.recognize_google(r.listen(source, en_thresh_new=1000, forced_buffer_count=10,
                                                       phrase_time_limit=phrase_time_limit if not ceci._music_is_active else 6)).lower()
                if ceci.not_talking(listen_time):
                    input_q.put(text)
                else:
                    ceci.plog("Voice was activated during listen", print_=True)

            except sr.UnknownValueError as e:
                print(e)


def analyze(ceci, input_q):
    r = sr.Recognizer()
    mic = ceci.get_mic()
    phrase_time_limit = 20

    ceci.play_sound('Hello, Joseph.')
    ceci.plog("Ready to listen...")

    last_hotword_time = 0
    while True:
        # if input_q.empty(): continue
        # audio= input_q.get()

        with mic as source:
            try:
                # listen_time= time.time()
                audio = r.recognize_google(
                    r.listen(source, en_thresh_new=1000,
                             forced_buffer_count=10,
                             phrase_time_limit=phrase_time_limit if not ceci._music_is_active else 6)).lower()
                # if ceci.not_talking(listen_time): input_q.put(text)
                # else: ceci.plog("Voice was activated during listen", print_= True)

            except sr.UnknownValueError as uve:
                ceci.plog("Got Unknown Value Error", obj=uve)

            else:
                keywords, product = ceci.get_audio_score(audio)
                ceci.plog(audio, keywords, product)
                ceci.plog(f"Text: {audio} | Keywords: {keywords} | Audio Score: {product}".replace("%", ""))

                if (got_hotword := product % 2 == 0) or time.time() - last_hotword_time < 10:
                    while True:
                        try:
                            taken, func_taken = ceci.execute_command(audio, keywords, product)
                            ceci.plog(f"Taken: {taken} | Function: {func_taken}")
                            if taken or got_hotword:
                                last_hotword_time = time.time()
                                if ceci._music_is_active and not (
                                        'spotify' in keywords and 'volume' in keywords): ceci.start_temp_sound_timer()
                                if ceci._respond:
                                    ceci._respond = False
                                    ceci.play_sound("I'm listening?")
                        except SpotifyException as spe:
                            ceci.plog("Got Spotify Exception", obj=spe)
                            ceci.reauth_spotify()
                        else:
                            break


if __name__ == '__main__':
    ceci = Cecilia()
    input_q = Queue()

    # Thread(target= listen, args= ((ceci, input_q),), daemon= True).start()
    analyze(ceci, input_q)
