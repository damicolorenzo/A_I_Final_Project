import warnings
warnings.filterwarnings("ignore", "\nPyarrow", DeprecationWarning)
import pandas as pd
import numpy as np
from collections import defaultdict #defaultdict is an unordered collection of data values that are used to store data values like a map
from scipy.spatial.distance import cdist

class Recommender:
    number_cols = ['valence', 'year', 'acousticness', 'danceability', 'duration_ms', 'energy', 'explicit',
    'instrumentalness', 'key', 'liveness', 'loudness', 'mode', 'popularity', 'speechiness', 'tempo']

    def __init__(self, spotify):
        self.sp = spotify

    def get_track_info(self, track_id):
        """ 
        * Preleva nome e data di incisione di una traccia
        * Dato in input un id_traccia ritorna una lista contenete l'oggetto {'name': nome, 'year': anno} 
        * Input track_id
        * Output [{'name': nome, 'year': anno}]
        """
        # Preleva le informazioni sulla traccia
        track_info = self.sp.track(track_id)

        # Estrae il nome e l'anno di uscita dalla risposta
        name = track_info['name']
        year = int(track_info['album']['release_date'][:4])

        # Crea un dizionario con le informazioni desiderate
        track_dict = {'name': name, 'year': year}
        # Restituisce una lista di oggetti costruiti come descritto in alto
        return track_dict

    def get_track_id(self, track_info):
        """ 
        * Preleva l'id della traccia
        * Dato in input un oggetto con informazioni della traccia ritorna None oppure l'id della traccia 
        * Input oggetto {'name': nome, 'year': anno}
        * Output track_id 
        """
        # Preleva dall'oggetto track_info il nome della traccia
        track_name = track_info['name']
    
        # Preleva dall'oggetto track_info l'anno di incisione della traccia
        release_year = int(track_info['year'])
    
        # Effettua la ricerca 
        search_results = self.sp.search(q=f'track:{track_name} year:{release_year}', type='track', limit=1)

        # Estrai l'ID della prima traccia trovata
        if search_results['tracks']['items']:
            track_id = search_results['tracks']['items']
            return track_id
        else:
            return None

    def find_song(self, name, year):
        """
        * Ricerca la canzone tramite nome e anno di incisione 
        * Dati nome e anno di incisione di una traccia ritorna None oppure un oggetto con le informazioni della canzone e le informazioni audio
        * Input nome e anno di incisione 
        * Output oggetto con informazioni relative alla canzone
        """
        song_data = defaultdict()
        
        # Effettua la ricerca 
        results = self.sp.search(q= 'track: {} year: {}'.format(name,year), limit=1)
        if results['tracks']['items'] == []:
            return None

        # Preleva l'id della traccia 
        results = results['tracks']['items'][0]
        track_id = results['id']
        # Preleva tramite l'id le informazioni audio della traccia 
        audio_features = self.sp.audio_features(track_id)[0]

        # Popolamento del dizionario
        song_data['name'] = [name]
        song_data['year'] = [year]
        song_data['explicit'] = [int(results['explicit'])]
        song_data['duration_ms'] = [results['duration_ms']]
        song_data['popularity'] = [results['popularity']]

        for key, value in audio_features.items():
            song_data[key] = value
        # Ritorna un DataFrame con le informazioni della canzone 
        return pd.DataFrame(song_data).squeeze() #conversione da DataFrame a Series

    def get_song_data(self, song, spotify_data):
        """ 
        * Ricerca le infomrazioni della canzone nel dataset e nel caso in cui non le trova le ricerca tramite la funzione find_song
        * Input oggetto {'name': nome, 'year': anno} e puntatore al dataset
        * Output informazioni riguardo la canzone 
        """
        # Ricerca nel dataset (spotify_data)
        try:
            song_data = spotify_data[(spotify_data['name'] == song['name']) 
                                    & (spotify_data['year'] == song['year'])].iloc[0]
            
            if isinstance(song_data,pd.DataFrame): 
                song_data = song_data.squeeze() #conversione da DataFrame a Series
            return song_data 
        except IndexError:
            # Ricerca tramite le funzione find_song
            return self.find_song(song['name'], song['year'])

    def get_mean_vector(self, song_list, spotify_data):
        """
        * Genera il vettore delle medie 
        * Input lista di canzoni e puntatore al dataset
        * Output vettore delle medie 
        """
        song_vectors = []
        
        for song in song_list:
            song_data = self.get_song_data(song, spotify_data)
            if song_data is None:
                print('Warning: {} does not exist in Spotify or in database'.format(song['name']))
                continue
            song_vector = song_data[self.number_cols].values # contiene tutti i valori numerici 
            song_vectors.append(song_vector) # contiene tutti i valori numerici di tutte le canzoni (matrice composta da vettori numerici)
        
        song_matrix = np.array(list(song_vectors)) # costruzione di una matrice con i valori delle canzoni
        return np.mean(song_matrix, axis=0) # media di ogni valore 

    def flatten_dict_list(self, dict_list):
        """ 
        * Fonde in un unico dizionario i nomi e le date di incisione di diverse canzoni
        * Input oggetto [{'name': nome, 'year': anno}]
        * Output oggetto {'name': [nome], 'year': [anno]}
        """
        flattened_dict = defaultdict()
        print("dict_list", dict_list)
        for key in dict_list[0].keys():
            flattened_dict[key] = []
        
        for dictionary in dict_list:
            for key, value in dictionary.items():
                flattened_dict[key].append(value)
        return flattened_dict

    def recommend_songs(self, song_list, n_songs=10):
        """
        * Effettua la raccomandazione 
        * Input lista di canzoni [{'name': nome, 'year': anno}]
        * Output [{'name': 'name1', 'year': year1, 'artists': "artists"}...]
        """
        metadata_cols = ['name', 'year', 'artists']
        song_dict = self.flatten_dict_list(song_list)
        song_center = self.get_mean_vector(song_list, self.spotify_data)
        
        scaler = self.song_cluster_pipeline.steps[0][1] # Scaler utilizzato (StandardScaler)
        scaled_data = scaler.transform(self.spotify_data[self.number_cols]) # Perform standardization by centering and scaling 
        scaled_song_center = scaler.transform(song_center.reshape(1, -1)) #vettore colonna

        distances = cdist(scaled_song_center, scaled_data, 'cosine') #vettore colonna distanze
        index = list(np.argsort(distances)[:, :n_songs][0]) #preleva i primi 10 elementi

        rec_songs = self.spotify_data.iloc[index] #preleva le righe dal dataset corrispondenti agli indici
        rec_songs = rec_songs[~rec_songs['name'].isin(song_dict['name'])] #controlla se le canzoni trovate dalla selezione sono presenti in song list
        return rec_songs[metadata_cols].to_dict(orient='records') #ritorna gli attributi name, year e artists delle canzoni trovate  
    
    def setSongClusterPipeline(self, scp):
        self.song_cluster_pipeline = scp

    def setData(self, data):
        self.spotify_data = data