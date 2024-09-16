import spotipy  #Spotipy is a lightweight Python library for the Spotify Web API.
from spotipy.oauth2 import SpotifyClientCredentials, SpotifyOAuth

SPOTIPY_CLIENT_ID = '7efe7f8ef16a4882801c706f94b410f8'
SPOTIPY_CLIENT_SECRET = '0bf8a6c1df6a4b88a9aeeb2aefa2a2ed'
SPOTIPY_REDIRECT_URI = 'http://localhost:5000/callback'
SCOPE = 'playlist-read-private'
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=SPOTIPY_CLIENT_ID,
                                               client_secret=SPOTIPY_CLIENT_SECRET,
                                               redirect_uri=SPOTIPY_REDIRECT_URI,
                                               scope=SCOPE))

# Ottieni le playlist dell'utente corrente
playlists = sp.current_user_playlists()

playlist_data = {}

# Per ogni playlist ottenuta
for playlist in playlists['items']:
    # Ottieni l'ID della playlist
    playlist_id = playlist['id']
    # Ottieni il nome della playlist
    playlist_name = playlist['name']
    # Ottieni le tracce della playlist
    tracks = sp.playlist_tracks(playlist_id)
    # Lista per memorizzare le canzoni della playlist
    playlist_tracks = []
    # Per ogni traccia nella playlist
    for track in tracks['items']:
        # Ottieni il nome della canzone
        track_name = track['track']['name']
        # Aggiungi il nome della canzone alla lista delle tracce della playlist
        playlist_tracks.append(track_name)
    # Aggiungi la playlist e le tracce corrispondenti al dizionario playlist_data
    playlist_data.update({playlist_name:playlist_tracks})

# Stampa il dizionario contenente le playlist e le relative canzoni
""" for playlist_name, tracks in playlist_data.items():
    print(f"Playlist: {playlist_name}")
    print("Canzoni:")
    for track in tracks:
        print(f"- {track}")
    print() """