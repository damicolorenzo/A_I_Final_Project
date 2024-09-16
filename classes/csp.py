from classes.CSP.cspProblem import Variable, Constraint, CSP
from classes.CSP.spotify_json import playlist_data
from classes.CSP.searchGeneric import Searcher1
from classes.CSP.cspSearch import Search_from_CSP

class csp:

    def __init__(self, songs):
        """
        Genera un oggetto CSP ed effettua il set di dict che contiene il 
        risultato del csp 
        """
        self.songs = songs
        Canzone = Variable('Canzone', self.get_list(self.songs))
        Playlist = Variable('Playlist',  self.in_playlist())
        problem = CSP("problem", {Canzone, Playlist}, 
               [
                    Constraint([Canzone, Playlist], self.func)
               ]) 
        searcher = Searcher1(Search_from_CSP(problem))
        self.dict = searcher.search() 

    def get_list(self, songs):
        """
        * Preleva i nomi delle canzoni 
        * Data in input una lista di oggetti ritorna una lista di titoli di canzoni
        * Input: [{'name':'value1', {}, ...}, ...] output ['name1', 'name2', ...]
        """
        return_list = list()
        for song in songs:
            return_list.append(song['name'])
        return return_list
    
    def get_playlist(self, playlist):
        """
        * Preleva le canzoni da una playlist
        * Dato in input il nome di una playlist ritorna una lista di canzoni (canzoni della playlist)
        """
        list_of_songs = list()
        for playlist_tracks in playlist_data[playlist]:
            list_of_songs.append(playlist_tracks)
        return list_of_songs
    
    #prende in ingresso un insieme di canzoni e ritorna il match canzone playlist prendendo le playlist dell'utente
    def in_playlist(self):
        """ 
        Preleva le playlist di un utente
        """
        list_of_playlist = list()
        for playlist_name in playlist_data:
                list_of_playlist.append(playlist_name)
        return list_of_playlist
    
    def func(self, song, playlist):
        """
        * Funzione di servizio del CSP 
        * Permette di controllare se la canzone è nella playlist
        """
        if song in self.get_playlist(playlist): 
            return True
        else: 
            return False
    
    def remove_from_dict(self):
        """ 
        * Rimuove le canzoni dal dizionario di oggetti canzone 
        * Dizionario oggetto canzoni del tipo [{'name':'value1', {}}, ...]
        * Ritorna una coppia di oggetti (corretti e rimossi)
        """
        solution = self.get_list(self.songs)
        removed_songs_names = []
        for e in self.dict:
            for el in e.arc.to_node:
                if el.name == 'Canzone':
                    solution.remove(e.arc.to_node[el])
        solution_dict = self.songs
        for e in self.songs:        
            if e["name"] not in solution:
                solution_dict.remove(e)
                removed_songs_names.append(e)
        return solution_dict, removed_songs_names   
    