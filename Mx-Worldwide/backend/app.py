from flask import Flask, request,jsonify
from flask_cors import CORS
from spotipy.oauth2 import SpotifyOAuth,SpotifyClientCredentials
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

    sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(client_id=config.client_id, client_secret=config.client_secret))

    # print("Current track: " + track)
    result = sp.search(q='track:'+track, type='track', limit=1)
    songID = result['tracks']['items'][0]['id']
    # print("ID: ", songID)

    trackURL = sp.track(songID)['preview_url']

    return trackURL

if __name__ == '__main__':
    app.run(debug=True,port="3052")