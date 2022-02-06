from config import Directories, Spotify_Credentials
from exceptions import MicNotFoundException
import logging
import speech_recognition as sr
import pandas as pd
import webbrowser as wb
import os
import sys
from math import prod
import time
import datetime
import spotipy
from threading import Timer


class Helper():
    def __init__(self):
        self._dir = Directories
        self._mic = 'Yeti'
        self._playsound_time = 0

        self._light_socket_info = '192.168.1.27', 1234
        self._light_dictionary = pd.read_excel(os.path.join(self._dir.UTILITIES, "lightcipher.xlsx"), index_col='num')[
            'role'].to_dict()

        if not os.path.isdir('logs'): os.mkdir('logs')
        logging.basicConfig(filename=f"logs/client-{datetime.datetime.now().strftime('%Y-%m-%d %H%M%S')}.log",
                            level=logging.INFO, filemode='w', format='%(asctime)-15s `Cecilia`: %(message)s')

    def plog(self, text: str, obj=None, print_=True):
        '''Adds `text` to the log. If plog, then `text` will be printed.'''
        if print_: print(text)
        logging.info(f"{text} {'-- Object: %s' if obj else '%s'}", obj if obj else '')

    def get_mic(self, mic_name: str = str()):
        if not mic_name: mic_name = self._mic

        pyaud = sr.Microphone().get_pyaudio().PyAudio()
        for i in range(pyaud.get_device_count()):
            device_info = pyaud.get_device_info_by_index(i)
            if mic_name in (device_name := device_info['name']):
                self.plog("setting microphone", obj=device_name, print_=False)
                return sr.Microphone(device_index=i)

        raise MicNotFoundException

    def not_talking(self, listen_time):
        return True if listen_time >= self._playsound_time else False

    def open_link(self, link):
        print(link)
        wb.get().open_new_tab(link)

    def txt_to_number(self, audio):
        '''Turns string into number value.'''
        return int(''.join([k for k in audio if k.isdigit()]))


class Spotify():
    def __init__(self):
        self._SC = Spotify_Credentials
        self._SPOT = spotipy.Spotify(auth=self.get_token())
        self._active_device = self.get_active_device_info()
        self._music_is_active = False

        self._reset_sound = False
        self._temp_sound = 0
        self._temp_sound_timer = Timer(0, int)
        self.start_temp_sound_timer()

    def get_token(self):
        sc = self._SC
        args = sc.USERNAME, sc.SCOPE, sc.CLIENT_ID, sc.CLIENT_SECRET, sc.REDIRECT_URI
        try:
            token = spotipy.util.prompt_for_user_token(*args)
        except:
            os.remove(f".cache-{sc.USERNAME}")
            token = spotipy.util.prompt_for_user_token(*args)
        return token

    def reauth_spotify(self):
        """Authenticates spotify object."""
        self._SPOT.set_auth(self.get_token())

    def get_active_device_info(self):
        for device in self._SPOT.devices().get('devices'):
            if (active := device.get('is_active')) or device.get('name') == 'DESKTOP-BNTDFT9':
                self._music_is_active = active
                break
        else:
            device = dict()
        self._active_device = device
        return device

    def get_spotify_volume(self):
        return int(self.get_active_device_info().get('volume_percent'))

    def set_spotify_volume(self, volume, temp=False):
        if not temp and self._temp_sound_timer.is_alive(): self._temp_sound_timer.cancel()
        self._SPOT.volume(volume, self._active_device.get('id'))

    def start_temp_sound_timer(self):
        if self._temp_sound_timer.is_alive():
            volume_arg = self._temp_sound_timer.args
            self._temp_sound_timer.cancel()
        else:
            volume_arg = (self.get_spotify_volume(),)
        self.set_spotify_volume(30, temp=True)
        self._temp_sound_timer = Timer(10, self.set_spotify_volume, args=volume_arg)
        self._temp_sound_timer.start()

    def play_song(self, cmd: str = str()):
        device_id = self._active_device.get('id')
        if not cmd:
            self._SPOT.start_playback(device_id=device_id)
            self._music_is_active = True
        elif 'pause' in cmd:
            self._SPOT.pause_playback(device_id=device_id)
            self._music_is_active = False
        elif 'next' in cmd:
            if 'shuffle' in cmd:
                self._SPOT.shuffle(False, device_id=device_id)
                self._SPOT.shuffle(True, device_id=device_id)
            self._SPOT.next_track(device_id=device_id)

        elif 'previous' in cmd:
            self._SPOT.previous_track(device_id=device_id)
        else:
            self._SPOT.add_to_queue(cmd, device_id=device_id)

    def search_song(self, audio):
        '''Returns song URI, song name, and artist name from search.'''
        play_index, by_index = audio.find('play') + 5, audio.find('by')
        song, artist = (audio[play_index:], None) if by_index == -1 else (
        audio[play_index: by_index - 1], audio[by_index + 3:])

        results = self._SPOT.search(q=f"track:{song} {artist}", type='track')
        track = results['tracks']['items'][0]
        # print(track['artists'])
        uri = track['uri']
        song = track['name']
        artists = [artists.get('name') for artists in track['artists']]
        artist = artists[
            0] if artists else None  # 'and'.join(artists) if len(artists) < 3 else ', '.join(artists[:-1]) + f', and {artists[-1]}'
        return uri, song, artist
