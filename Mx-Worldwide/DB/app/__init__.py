from flask import Flask, jsonify, request, abort
from pymongo import MongoClient
from flask_cors import CORS
import flask_login

app = Flask(__name__)
app.config['JSON_SORT_KEYS'] = False
#CORS(app, resources={r"/*": {"origins": "*"}})

#client = MongoClient('localhost', 27017, username='username', password='password')
client = MongoClient('localhost', 27017)


def get_database():
    return client['Mx_world']


db = get_database()
users = db.users
musics = db.musics
mh = db.music_history
comments = db.comments


#begin code used for login
login_manager = flask_login.LoginManager()
login_manager.init_app(app)


@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"

def get_database():
    return client['Mx_world']



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



if __name__ == "__main__":   
  
   # Get the database
   db = get_database()



    