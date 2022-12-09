from flask import Flask, request,jsonify, redirect
from flask_cors import CORS
from spotipy.oauth2 import SpotifyClientCredentials
import spotipy, lyricsgenius, deepl
import config
import oauth2 as oauth
import requests

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

        trackURL,albumURL = spotipyID(songName, artist)
        return jsonify({'trackURL': trackURL,
                        'albumArt': albumURL})
    else:
        return jsonify({'trackURL': 'No track',
                        'albumArt': 'No album'})

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

@app.route('/oauth/signin', methods=['POST', 'GET'])
def signin():
    if request.method == 'GET':
        consumerkey = config.consumer_key
        consumersecret = config.consumer_secret

        #url = "https://api.twitter.com/oauth/request_token?oauth_callback=http%3A%2F%2Flocalhost%3A4200%2F"
        #headers = {"oauth_consumer_key": consumerkey}
        #response = requests.post(url = url, headers = headers)
        #print(response.text)
        


        url = "https://api.twitter.com/oauth/request_token"

        payload={}
        headers = {
        'Authorization': 'OAuth oauth_consumer_key= ' + config.consumer_key + ',oauth_signature_method="HMAC-SHA1",oauth_timestamp="1670545136",oauth_nonce="g9VbzEP1Q4K",oauth_version="1.0",oauth_signature="QPkMhLWxc4RaktHpgU0tSCHC1TQ%3D"','Cookie': 'guest_id=v1%3A167028018557823366'
        }

        response = requests.request("POST", url, headers=headers, data=payload)
        split = response.text.split("&", 2)

        print(response.text)
        print(response)
        print(split)
        config.oauth_token = split[0][12:]
        config.oauth_token_secret = split[1][19:]

        #print(oauth_token)
        #print(oauth_token_secret)



        return jsonify({'link': "https://api.twitter.com/oauth/authorize?oauth_token=" + config.oauth_token})
    else:
        return jsonify({'link': 'localhost:4200'})

@app.route('/oauth/signin2', methods=['POST', 'GET'])
def signin2():
    if request.method == 'POST':
        oauth_token = request.get_json()['oauth_token']
        oauth_verifier = request.get_json()['oauth_verifier']

        #print(oauth_token)
        #print(oauth_verifier)
        url = "https://api.twitter.com/oauth/access_token?oauth_token=" + oauth_token + "&oauth_verifier=" + oauth_verifier

        payload={}
        headers = {
        'Authorization': 'OAuth oauth_consumer_key="' + config.consumer_key + '",oauth_token="' + config.oauth_token + '",oauth_signature_method="HMAC-SHA1",oauth_timestamp="1670376194",oauth_nonce="drlAwytFQ1M",oauth_version="1.0",oauth_signature="3PsILi0UX5W2kt5pxwDJNEX1ePg%3D"',
        }

        response = requests.request("GET", url, headers=headers, data=payload)
        #print(response)
        #print(response.text)

        return jsonify({'status': 'Ok'})
    else:
        return jsonify({'status': 'Failed'})


def spotipyID(track, artist):
    sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(client_id=config.client_id, client_secret=config.client_secret))
    result = sp.search(q='track:'+track+' artist:'+artist, type='track', limit=1)

    trackURL = result['tracks']['items'][0]['preview_url']
    albumURL = result['tracks']['items'][0]['album']['images'][0]['url']

    return trackURL, albumURL

if __name__ == '__main__':
    app.run(debug=True,port="3052")