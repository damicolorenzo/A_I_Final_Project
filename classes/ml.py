from classes.dataCluster import dataCluster
from classes.recommender import Recommender
from classes.csp import csp

class ML:

    def __init__(self, spotify, view):
        self.d = dataCluster(view)
        self.r = Recommender(spotify)
        self.similar_list = list()
        self.songs = []
        self.removed_songs = []
        
    def generation(self):
        """
        Metodo che permette di creare un collegamento con il dataCluster che gestisce i dataset e Recommender che gestisce il modello  
        """
        self.r.setSongClusterPipeline(self.d.getSongClusterPipeline())
        self.r.setData(self.d.getData()) 
    
    def solving(self):
        """
        Metodo che permette di creare un CSP ed ottenere il risultato del CSP e anche ciò che è stato scartato
        """
        c = csp(self.songs)
        self.songs , self.removed_songs = c.remove_from_dict()
        
    def recommend(self, track_list):
        """
        Metodo che permette di generare una raccomandazione passando in input una traccia 
        """
        self.songs = []
        temp_list = []
        if type(track_list) == 'string':
            track_list = [].append(track_list)
        for e in track_list:
            print("e", e)
            temp_list.append(self.r.get_track_info(e))
            print(temp_list)
        self.songs = self.r.recommend_songs(temp_list) 
    
    def printing(self):
        """
        Metodo di conversione da lista di canzoni (titoli) a lista di canzoni (id)
        """
        self.similar_list = []
        for e in self.songs:
            if self.r.get_track_id(e) is not None:
                x = self.r.get_track_id(e)[0]
                self.similar_list.append(x)
            else:
                e.update({'album':None})
                self.similar_list.append(e)
        self.removed_list = []
        for e in self.removed_songs:
            if self.r.get_track_id(e) is not None:
                self.removed_list.append(self.r.get_track_id(e)[0])