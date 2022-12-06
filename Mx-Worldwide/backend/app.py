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

        trackURL = spotipyID(songName, artist)
        return jsonify({'trackURL': trackURL})
    else:
        return jsonify({'trackURL': 'No track URL'})

@app.route('/api/lyrics', methods=['POST', 'GET'])
def lyrics():
    if request.method == 'POST':
        artist = genius.search_artist(request.get_json()['artist'], max_songs=0)
        song = genius.search_song(request.get_json()['songName'], artist.name)

        return jsonify({'artistName': artist.name,
                        'songName': song.title,
                        'originalLyrics': song.lyrics})
    else:
        return jsonify({'artistName': 'No artist',
                        'songName': 'No song',
                        'originalLyrics': 'No lyrics'})

@app.route('/api/translate', methods=['POST', 'GET'])
def translate():
    if request.method == 'POST':
        lyrics = request.get_json()['originalLyrics']
        target_lang = request.get_json()['targetLang']
        translated = translator.translate_text(lyrics, target_lang=target_lang)

        originalJson = request.get_json()
        originalJson['translatedLyrics'] = translated.text
        originalJson['targetLang'] = target_lang

        return jsonify(originalJson)
    else:
        originalJson = {'artistName': 'No artist',
                        'songName': 'No song',
                        'originalLyrics': 'No lyrics'}

        originalJson['translatedLyrics'] = 'No lyrics'
        originalJson['targetLang'] = 'No language'

        return jsonify(originalJson)


def spotipyID(track, artist):
    sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(client_id=config.client_id, client_secret=config.client_secret))
    result = sp.search(q='track:'+track+' artist:'+artist, type='track', limit=1)
    trackURL = result['tracks']['items'][0]['preview_url']

    return trackURL

if __name__ == '__main__':
    app.run(debug=True,port="3052")