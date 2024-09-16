import json
import spotipy  #Spotipy is a lightweight Python library for the Spotify Web API.
from spotipy.oauth2 import SpotifyClientCredentials

class Configuration:

    def __init__(self):
        config_file = open("config.txt", "r")
        string = config_file.read()
        dizionario = json.loads(string)
        self.sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(client_id=dizionario['client_id'],
                                                            client_secret=dizionario['client_secret'])) 
        if 'view' in dizionario:
            if  dizionario['view'] == "True":
                self.view = True
            elif dizionario['view'] == "False":
                self.view = False
        else:
            self.view = False


    def getSpotify(self):
        return self.sp
    
    def getView(self):
        return self.view