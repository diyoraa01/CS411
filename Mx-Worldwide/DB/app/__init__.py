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
u = db.users
music = db.musics
mh = db.music_history

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
    db['users'].insert_one({
        'name': re['name'],
        'gender': re['gender'],
        'language': re['language']
    })
    
    return jsonify(re, "Success"), 201


# get the user information by (user name or user id)?
@app.route('/get_user_info', methods=['GET'])
def get_user_info():
    name = 'test02'

    info = db.users.find_one({'name': name},{'name': 1, 'gender': 1, 'language': 1})

    return jsonify({
            'name': info['name'],
            'language': info['language'],
            'gender': info['gender']
        })


# get the user information by (user name or user id)?
@app.route('/get_user_mh', methods=['GET'])
def get_user_mh():
    name = 'test02'

    info = mh.find({'name': name}, {'musicname': 1, 'artist': 1})

    return jsonify({
            'musicname': info['musicname'],
            'artist': info['artist']
        })



###############################################
# Music part


# create a new music info after a user search a music
@app.route('/create_music', methods=['POST'])
def create_music():
    re = request.json
    db['music'].insert_one({
        'musicname': re['musicname'],
        'artist': re['artist'],
        'language': re['language'],
        'lyrics': re['lyrics']
    })
    

    return jsonify(re, "Success"), 201



# insert a music into user's music history
@app.route('/insert_music', methods=['POST'])
def insert_music():
    re = request.json
    user_name = re['user_name']
    music_name = re['music_name']
    artist = re['artist']

    mh_doc = {'user_name' : user_name, 'music_name' : music_name, 'artist': artist}

    count = mh.find(mh_doc).count()
    if (count != 0):
        mh.insert_one(mh_doc)
    

    return jsonify("Success")



# get lyrics in a specific language
@app.route('/get_lyrics', methods=['POST'])
def get_lyrics():
    re = request.json
    musicname = re['musicname']
    artist = re['artist']
    language = re['language']

    lyrics = db.users.find_one({'musicname': musicname, 'artist': artist, 'language': language},{'lyrics': 1})


    return jsonify({
            'lyrics': lyrics
        })



###############################################
# Comment part

'''

def add_comment(music_id,name , email, comment, date):
    
    comment_doc = { 'music_id' : music_id, 'name' : name, 'email' : email,'text' : comment, 'date' : date}
    return db.comments.insert_one(comment_doc)


def update_comment(comment_id, user_email, text, date):
    """
    Updates the comment in the comment collection. Queries for the comment
    based by both comment _id field as well as the email field to doubly ensure
    the user has permission to edit this comment.
    """
    # TODO: Create/Update Comments
    # Use the user_email and comment_id to select the proper comment, then
    # update the "text" and "date" of the selected comment.
    response = db.comments.update_one(
        { "comment_id": comment_id },
        { "$set": { "text ": text, "date" : date } }
    )

    return response


def delete_comment(comment_id, user_email):
    """
    Given a user's email and a comment ID, deletes a comment from the comments
    collection
    """

    response = db.comments.delete_one( { "_id": ObjectId(comment_id) } )
    return response

'''


if __name__ == "__main__":   
  
   # Get the database
   db = get_database()



    