from common import Helper, Spotify
import pandas as pd
import os, sys
import socket
from math import prod
from threading import Lock
from gtts import gTTS
import playsound
import time


class Cecilia(Helper, Spotify):

    def __init__(self):
        Helper.__init__(self)
        Spotify.__init__(self)

        df = pd.read_excel(os.path.join(self._dir.DATA, 'keywords.xlsx'))
        self._keyword_dict = dict(
            [(word, val) for word, val in df.set_index('word')['val'].to_dict().items() if not pd.isnull(word)])
        self._func_dict = dict(
            [(prod, getattr(self, func)) for prod, func in df.set_index('product')['func'].to_dict().items() if
             not pd.isnull(prod)])
        self._func_values = self._func_dict.keys()
        self.plog("keyword dict", obj=self._keyword_dict, print_=False)
        self.plog("function dict", obj=self._func_dict, print_=False)

        self._respond = False
        self._speak_lock = Lock()

    def execute_command(self, audio, keywords, score):
        '''Returns True if `product` mapped to a function, False if otherwise.'''
        return self.call_func(score, audio) if score != 2 or (func := self.ceci_respond)(audio) else (
        True, func.__func__)  # if score is 2, calls ceci_respond

    def get_audio_score(self, audio):
        kwd = self._keyword_dict
        keywords, primes = zipped if any(
            zipped := list(zip(*[(word, val) for word in audio.split() if (val := kwd.get(word))]))) else ([], [1])

        return keywords, prod(primes)

    def call_func(self, score, audio):
        if score := score * 2:
            for func_score in self._func_values:
                if score % func_score == 0:
                    self.plog("final function score", obj=func_score, print_=False)
                    func = self._func_dict[func_score]
                    func(audio)
                    return True, func.__func__
        return False, None

    def play_sound(self, audio):
        tts = gTTS(audio)
        file_path = os.path.join(self._dir.SOUND, 'play.mp3')
        with open(file_path, 'wb') as f:
            tts.write_to_fp(f)
            f.close()

        self._playsound_time = time.time()
        playsound.playsound(file_path, block=True)
        self._playsound_time = time.time()
        self.plog("playsound", obj=audio, print_=False)
        os.remove(file_path)

    def ceci_respond(self, audio):
        if len(audio.split()) == 1: self._respond = True
        # self.play_sound("I'm listening?")

    def search(self, audio):
        splaud = audio.split()
        keyword, *_ = (word for word in splaud if word in ['google', 'up', 'lookup', 'search'])
        link = 'www.google.com/search?q=' + '+'.join(splaud[splaud.index(keyword) + 1:])
        self.open_link(link)

    def news(self, audio):
        self.play_sound("Here is today's news.")
        self.open_link('https://www.wsj.com/')

    def set_output_device(self, audio):
        h = 'Main Speakers' if 'speaker' in audio else 'A50 Game'
        os.system(f'cmd /c "nircmd setdefaultsounddevice "{h}" 1 & nircmd setdefaultsounddevice "A50 Voice" 2"')
        self.play_sound(f'{h} set to default playback device.')

    def lights(self, audio):
        assert audio
        if 'choice' in audio or 'option' in audio:
            print("########## LIGHT CHOICES ##########")
            for num, role in self._light_dictionary.items():
                print(f"{num}: {role}")
            print("###################################")
        else:
            if update := ('update' in audio or 'refresh' in audio):
                os.system(f'cmd /c "{os.path.join(self._dir.UTILITIES, "updatewintel.bat")}"')
                audio = 'update lights'

            try:
                light_socket = socket.socket()
                light_socket.connect(self._light_socket_info)
                self.plog("connected to lights, sending audio", obj=audio, print_=False)
                light_socket.send(audio.encode())
                light_socket.close()
                sent = True
            except:
                self.play_sound("Failed to connect to light client...")
                self.plog("failed to connect to light client")
                sent = False

            if update: self.play_sound(f"Light files{' and client ' if sent else ' '}were successfully updated!")

    def spotify_interpreter(self, audio):
        if 'volume' in audio:
            if 'current' in audio:
                speech = f"Current Spotify volume is {self.get_spotify_volume()}%."
            else:
                if 'mute' in audio:
                    volume = 0
                else:
                    volume = int(self.txt_to_number(audio))
                self.set_spotify_volume(volume)
                speech = f"Spotify volume changed to {volume}%."

            self.play_sound(speech)
        else:
            cmd = str()
            if 'play' in audio and not 'music' in audio:
                cmd, song, artist = self.search_song(audio)
                self.play_sound(f"{song} by {artist} added to the queue.")

            elif 'pause' in audio:
                cmd = 'pause'

            elif 'next' in audio:
                cmd = 'next'

            elif 'shuffle' in audio:
                cmd = 'next shuffle'

            elif 'previous' in audio:
                cmd = 'previous'

            self.play_song(cmd=cmd)

    def change_system_volume(self, audio):
        if 'mute' in audio:
            os.system('cmd /c "nircmd setsysvolume 0"')
            self.play_sound("System sounds are muted. This is a little silly don't you think?")
        else:
            volume = ((volume_num := self.txt_to_number(
                audio)) / 100) * 65535  # convert to windows volume representation
            os.system(f'cmd /c "nircmd setsysvolume {volume}"')
            self.play_sound(f"System volume changed to {volume_num}%.")

    def terminate_process(self, audio):
        print('terminate process')

    def lock_computer(self, audio):
        print('lock computer')

    def reboot(self, audio):
        self.plog("got reboot command...", print_=False)
        self.play_sound("See you in a sec...")
        os.execv(sys.executable, [sys.executable, "main.py"] + sys.argv)

    def exit(self, audio):
        self.plog("got exit command...", print_=False)
        self.play_sound("Sleepy night night time.")
        exit()
