from flask import Flask, render_template, request
from classes.ml import ML
from classes.configuration import Configuration
# Configurazione dell'applicazione Flask
app = Flask(__name__)
# Configurazione dell'interfaccia con le API
spotify = Configuration().getSpotify()
view = Configuration().getView()
# Configurazione di un oggetto ML che gestisce il modello
ml = ML(spotify, view)
ml.generation()
history_track_list = []
# Pagina iniziale
@app.route('/')
def index():
    return render_template('index.html')
# Pagina di ricerca
@app.route('/search', methods=['POST'])
def search():
    query = request.form['query']
    results = spotify.search(q=query, type='track')
    tracks = results['tracks']['items']
    return render_template('search.html', tracks=tracks)

# Pagina per gestire l'auto completamento
@app.route('/autocomplete', methods=['POST'])
def autocomplete():
    query = request.form['query']
    results = spotify.search(q=query, type='track', limit=5)  # Limita i risultati a 5 per la demo
    tracks = results['tracks']['items']
    return render_template('autocomplete.html', tracks=tracks)

# Pagina per selezionare una canzone
@app.route('/select', methods=['POST'])
def select():
    track_id = request.form['track_id']
    track_name = request.form['track_name']
    return render_template('select.html', track_id=track_id, track_name=track_name)

# Pagina per la riproduzione della canzone selezionata
@app.route('/createList', methods=['POST'])
def createList():
    global history_track_list
    track_id = request.form['track_id']
    tpe = request.form['type']
    if tpe == "reset":
        history_track_list = []
    history_track_list.append(track_id) 
    return render_template('createList.html', track_list=history_track_list)

# Pagina per la riproduzione della canzone selezionata
@app.route('/play', methods=['POST'])
def play():
    track_id = request.form['track_id']
    return render_template('play.html', track_id=track_id)

@app.route('/similar')
def similar():
    global history_track_list
    #track_list = request.form['track_list']
    ml.recommend(history_track_list) 
    ml.solving()
    ml.printing()
    track_list = ml.similar_list
    ex_list = ml.removed_list
    #print(track_list)
    return render_template('similar.html', similar_tracks=track_list, removed_tracks=ex_list)

if __name__ == '__main__':
    app.run(debug=True)

#Per eseguire l'applicazione utilizzare il comando 
#flask --app index run --debugger