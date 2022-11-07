from flask import Flask, request, redirect, url_for,jsonify
from flask_cors import CORS
from spotipy.oauth2 import SpotifyOAuth
import requests,sys,spotipy
import config

app = Flask(__name__)
CORS(app)

@app.route('/api/hello')
def hello():
    return jsonify({'text': 'Hello World!'})


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