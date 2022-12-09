from flask import Flask, request,jsonify, redirect
from flask_cors import CORS
from spotipy.oauth2 import SpotifyClientCredentials
import spotipy, lyricsgenius, deepl
import config
import oauth2 as oauth
import requests
from pymongo import MongoClient



app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})
app.config['JSON_SORT_KEYS'] = False

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
        url = "https://api.twitter.com/oauth/request_token"
        payload={}
        headers = {
        'Authorization': 'OAuth oauth_consumer_key= ' + config.consumer_key + ',oauth_signature_method="HMAC-SHA1",oauth_timestamp="1670545136",oauth_nonce="g9VbzEP1Q4K",oauth_version="1.0",oauth_signature="QPkMhLWxc4RaktHpgU0tSCHC1TQ%3D"','Cookie': 'guest_id=v1%3A167028018557823366'
        }

        response = requests.request("POST", url, headers=headers, data=payload)
        split = response.text.split("&", 2)
        config.oauth_token = split[0][12:]
        config.oauth_token_secret = split[1][19:]

        return jsonify({'link': "https://api.twitter.com/oauth/authorize?oauth_token=" + config.oauth_token})
    else:
        return jsonify({'link': 'localhost:4200'})

@app.route('/oauth/signin2', methods=['POST', 'GET'])
def signin2():
    if request.method == 'POST':
        oauth_token = request.get_json()['oauth_token']
        oauth_verifier = request.get_json()['oauth_verifier']

        url = "https://api.twitter.com/oauth/access_token?oauth_token=" + oauth_token + "&oauth_verifier=" + oauth_verifier

        payload={}
        headers = {
        'Authorization': 'OAuth oauth_consumer_key="' + config.consumer_key + '",oauth_token="' + config.oauth_token + '",oauth_signature_method="HMAC-SHA1",oauth_timestamp="1670376194",oauth_nonce="drlAwytFQ1M",oauth_version="1.0",oauth_signature="3PsILi0UX5W2kt5pxwDJNEX1ePg%3D"',
        }

        response = requests.request("GET", url, headers=headers, data=payload)




        return jsonify({'status': 'Ok'})
    else:
        return jsonify({'status': 'Failed'})


def spotipyID(track, artist):
    sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(client_id=config.client_id, client_secret=config.client_secret))
    result = sp.search(q='track:'+track+' artist:'+artist, type='track', limit=1)

    trackURL = result['tracks']['items'][0]['preview_url']
    albumURL = result['tracks']['items'][0]['album']['images'][0]['url']

    return trackURL, albumURL




############################################################################################################################

client = MongoClient('localhost', 27017)


def get_database():
    return client['Mx_world']


db = get_database()
users = db.users
musics = db.musics
mh = db.music_history
comments = db.comments





###############################################
# User part


# create a new user after login with OAuth
@app.route('/create_user', methods=['POST'])
def create_user():
    re = request.json
    users.insert_one({
        'name': re['name'],
        'gender': re['gender'],
        'language': re['language']
    })
    
    return jsonify(re, "Success"), 201


# get the user information of current user
@app.route('/get_user_info', methods=['GET'])
def get_user_info():
    name = 'test02'

    info = users.find_one({'name': name},{'name': 1, 'gender': 1, 'language': 1})

    return jsonify({
            'name': info['name'],
            'language': info['language'],
            'gender': info['gender']
        })


# get the user music history of current user
@app.route('/get_user_mh', methods=['POST'])
def get_user_mh():
    re = request.json
    name = re['name']

    list = mh.find({'user_name': name}, {'music_name': 1, 'artist': 1, 'language': 1, 'url': 1})
    print(list)
    info_doc = []
    for info in list:
        print(info)
        temp = {
            'musicname': info['music_name'],
            'artist': info['artist'],
            'language': info['language'],
            'url': info['url']
        }
        info_doc.append(temp)

    return jsonify(info_doc)



###############################################
# Music part


# create a new music info after a user search a music
@app.route('/create_music', methods=['POST'])
def create_music():
    re = request.json
    musics.insert_one({
        'musicname': re['musicname'],
        'artist': re['artist'],
        'language': re['language'],
        'lyrics': re['lyrics'],
        'url': re['url']
    })
    

    return jsonify(re, "Success")



# insert a music into user's music history
@app.route('/insert_music', methods=['POST'])
def insert_music():
    re = request.json
    user_name = re['user_name']
    music_name = re['music_name']
    artist = re['artist']
    language = re['language']
    url = re['url']

    mh_doc = {'user_name' : user_name, 'music_name' : music_name, 'artist': artist, 'language': language, 'url': url}

    mh.insert_one(mh_doc)
    

    return jsonify("Success")



# get lyrics in a specific language
@app.route('/get_lyrics', methods=['POST'])
def get_lyrics():
    re = request.json
    musicname = re['musicname']
    artist = re['artist']
    language = re['language']

    lyrics = musics.find_one({'musicname': musicname, 'artist': artist, 'language': language},{'lyrics': 1})


    return jsonify({
            'lyrics': lyrics['lyrics']
        })




if __name__ == '__main__':
    app.run(debug=True,port="3052")

    # Get the database
    db = get_database()