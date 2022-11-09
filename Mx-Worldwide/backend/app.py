from flask import Flask, request, redirect, url_for,jsonify
from flask_cors import CORS
from spotipy.oauth2 import SpotifyOAuth
import requests,sys,spotipy
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
        print(songName)
        trackURL = spotipyID(songName)
        return jsonify({'trackURL': trackURL})
    else:
        return jsonify({'trackURL': 'No track URL'})

def spotipyID(track):
    cid = config.client_id
    secret = config.client_secret
    uri = config.redirect_uri
    oathmanager = SpotifyOAuth(client_id=cid, client_secret=secret, redirect_uri=uri)
    sp = spotipy.Spotify(oauth_manager=oathmanager)

    print("Current track: " + track)
    result = sp.search(q='track:'+track, type='track', limit=1)
    songID = result['tracks']['items'][0]['id']
    print("ID: ", songID)

    trackURL = sp.track(songID)['preview_url']

    return trackURL

if __name__ == '__main__':
    app.run(debug=True,port="3052")