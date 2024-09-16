import warnings
warnings.filterwarnings("ignore", "\nPyarrow", DeprecationWarning)
import pandas as pd
import numpy as np
import plotly.express as px 
from sklearn.manifold import TSNE
from sklearn.decomposition import PCA
from sklearn.cluster import KMeans #K-means è un algoritmo di analisi dei gruppi partizionale che permette di suddividere un insieme di oggetti in k gruppi sulla base dei loro attributi
from sklearn.preprocessing import StandardScaler #Normalizzazione e standardizzazione di attributi/variabili/colonne (media = 0 e deviazione standard = 1)
from sklearn.pipeline import Pipeline #The purpose of the pipeline is to assemble several steps that can be cross-validated together while setting different parameters.


class dataCluster: 

    data = pd.read_csv("./dataset/data.csv")
    genre_data = pd.read_csv("./dataset/data_by_genres.csv")

    def __init__(self, view=False):
        if view:
            X = self.method1()
            self.method2(view, X)
            Y, song_cluster_pipeline = self.method3()
            self.method4(view, Y)
            self.song_cluster_pipeline = song_cluster_pipeline
        else:
            Y , song_cluster_pipeline = self.method3()
            self.song_cluster_pipeline = song_cluster_pipeline

    def method1(self):
        cluster_pipeline = Pipeline([('scaler', StandardScaler()), ('kmeans', KMeans(n_clusters=10))])
        X = self.genre_data.select_dtypes(np.number)
        cluster_pipeline.fit(X)
        self.genre_data['cluster'] = cluster_pipeline.predict(X)
        return X

    def method2(self, view, X):
        tsne_pipeline = Pipeline([('scaler', StandardScaler()), ('tsne', TSNE(n_components=2, verbose=1))])
        genre_embedding = tsne_pipeline.fit_transform(X)
        projection = pd.DataFrame(columns=['x', 'y'], data=genre_embedding)
        projection['genres'] = self.genre_data['genres']
        projection['cluster'] = self.genre_data['cluster']

        fig = px.scatter(
            projection, x='x', y='y', color='cluster', hover_data=['x', 'y', 'genres'])
        if view:
            fig.show()

    def method3(self):
        song_cluster_pipeline = Pipeline([('scaler', StandardScaler()), 
                                            ('kmeans', KMeans(n_clusters=20,
                                            verbose=False)) #n_clusters = 20 numero di cluster creati, verbose = False: non stampa informazioni extra
                                            ], verbose=False)

        Y = self.data.select_dtypes(np.number) #This selects only the columns in the DataFrame data that have numerical data types
        song_cluster_pipeline.fit(Y)
        song_cluster_labels = song_cluster_pipeline.predict(Y)
        self.data['cluster_label'] = song_cluster_labels
        return Y, song_cluster_pipeline

    def method4(self, view, Y):
        pca_pipeline = Pipeline([('scaler', StandardScaler()), ('PCA', PCA(n_components=2))])
        song_embedding = pca_pipeline.fit_transform(Y)
        projection = pd.DataFrame(columns=['x', 'y'], data=song_embedding)
        projection['title'] = self.data['name']
        projection['cluster'] = self.data['cluster_label']

        fig = px.scatter(
            projection, x='x', y='y', color='cluster', hover_data=['x', 'y', 'title'])
        if view:
            fig.show()

    def getSongClusterPipeline(self):
        return self.song_cluster_pipeline
    
    def getData(self):
        return self.data
    