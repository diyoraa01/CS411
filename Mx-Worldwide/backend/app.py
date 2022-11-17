from flask import Flask, request,jsonify
from flask_cors import CORS
from spotipy.oauth2 import SpotifyClientCredentials
from googletrans import Translator
import spotipy, lyricsgenius
import config

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

@app.route('/api/hello')
def hello():
    return jsonify({'text': 'Hello World!'})

@app.route('/api/search', methods=['POST', 'GET'])
def search():
    if request.method == 'POST':
        songName = request.get_json()['songName']
        # print(songName)
        trackURL = spotipyID(songName)
        return jsonify({'trackURL': trackURL})
    else:
        return jsonify({'trackURL': 'No track URL'})

@app.route('/api/lyrics', methods=['POST', 'GET'])
def lyrics():
    genius = lyricsgenius.Genius(config.GToken)
    if request.method == 'POST':
        artist = genius.search_artist(request.get_json()['artist'], max_songs=0)
        song = genius.search_song(request.get_json()['songName'], artist.name)
        return jsonify({'lyrics': song.lyrics})
    # Returns a song type which may give access to available translations 
    #  and translation API might not be needed for those that are available
    else:
        return jsonify({'lyrics': 'No lyrics'})

# @app.route('/api/translate', methods=['POST', 'GET'])
# def translate():
#     genius = lyricsgenius.Genius(config.GToken)
#     artist = genius.search_artist("azealia Banks", max_songs=0)
#     songlyrics = genius.search_song("Anna Wintour", artist.name)
#     translator = Translator()
#     translation = translator.translate("Hello World", dest="es")
#     return jsonify({'translation': translation.text})


def spotipyID(track):

    sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(client_id=config.client_id, client_secret=config.client_secret))

    # print("Current track: " + track)
    result = sp.search(q='track:'+track, type='track', limit=1)
    # print(result)
    trackURL = result['tracks']['items'][0]['preview_url']
    # print(trackURL)

    return trackURL

if __name__ == '__main__':
    app.run(debug=True,port="3052")