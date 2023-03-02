from credentials import Spotify_Credentials
import os

##### DIRECTORIES ######


class Directories:
    MAIN = os.getcwd()
    SOUND = os.path.join(MAIN, 'sounds')
    DATA = os.path.join(MAIN, 'data')
    BROWSER = os.path.join(MAIN, 'browser')
    UTILITIES = os.path.join(MAIN, 'utilities')
