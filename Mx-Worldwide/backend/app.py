from flask import Flask, request,jsonify
from flask_cors import CORS
from spotipy.oauth2 import SpotifyClientCredentials
import spotipy, lyricsgenius, deepl
import config

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

genius = lyricsgenius.Genius(config.GToken)
translator = deepl.Translator(config.DeeplAuth)

@app.route('/api/hello')
def hello():
    return jsonify({'text': 'Hello World!'})

@app.route('/api/search', methods=['POST', 'GET'])
def search():
    if request.method == 'POST':
        artist = request.get_json()['artist']
        songName = request.get_json()['songName']
        # print(songName)
        trackURL = spotipyID(songName)
        return jsonify({'trackURL': trackURL})
    else:
        return jsonify({'trackURL': 'No track URL'})

@app.route('/api/lyrics', methods=['POST', 'GET'])
def lyrics():
    if request.method == 'POST':
        artist = genius.search_artist(request.get_json()['artist'], max_songs=0)
        song = genius.search_song(request.get_json()['songName'], artist.name)
        return jsonify({'lyrics': song.lyrics})
    # Returns a song type which may give access to available translations 
    #  and translation API might not be needed for those that are available
    else:
        return jsonify({'lyrics': 'No lyrics'})

@app.route('/api/translate', methods=['POST', 'GET'])
def translate():
    if request.method == 'POST':
        lyrics = request.get_json()['lyrics']
        target_lang = request.get_json()['target_lang']
        # print(text)
        # print(target_lang)
        translated = translator.translate_text(lyrics, target_lang=target_lang)
        # print(translated)
        return jsonify({'translated': translated})
    else:
        return jsonify({'translated': 'No translation'})


def spotipyID(track, artist):
    sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(client_id=config.client_id, client_secret=config.client_secret))
    result = sp.search(q='track:'+track+' artist:'+artist, type='track', limit=1)
    trackURL = result['tracks']['items'][0]['preview_url']

    return trackURL

if __name__ == '__main__':
    app.run(debug=True,port="3052")