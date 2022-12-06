from flask import Flask, jsonify, request, abort
from pymongo import MongoClient
from flask_cors import CORS
import flask_login

app = Flask(__name__)
#CORS(app, resources={r"/*": {"origins": "*"}})

#client = MongoClient('localhost', 27017, username='username', password='password')
client = MongoClient('localhost', 27017)


def get_database():
    return client['Mx_world']


db = get_database()
u = db.users

#begin code used for login
login_manager = flask_login.LoginManager()
login_manager.init_app(app)


@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"

def get_database():
    return client['Mx_world']





###############################################


# create a new user after login with OAuth
@app.route('/create_user', methods=['POST'])
def create_user():
    re = request.json
    db['users'].insert_one({
        
        'name': re['name'],
        'gender': re['gender'],
        'language': re['language'],
        'music_history': []   
    })
    
    # user = User(name=request.json['name'], password=request.json['password']).save()
    return jsonify(re, "Success"), 201


# get the user information by (user name or user id)?
@app.route('/get_user', methods=['GET'])
def get_user():
    name = request.json

    return jsonify({'userinfo'}), 201




##########

'''
# create a new music info after a user search a music
@app.route('/create_music', methods=['POST'])
def create_music():
    re = request.json
    db['music'].insert_one({
        'musicname': re['musicname'],
        'author': re['author']
    })
    
    # user = User(name=request.json['name'], password=request.json['password']).save()
    return jsonify(re, "Success"), 201
'''

# insert a music into user's music history
@app.route('/insert_music', methods=['POST'])
def insert_music():
    re = request.json
    user = re['user']
    
    cur = db.users.find_one({'name': user},{"music_history":1})
    print(cur)
    v = cur['music_history']
    temp = {
        'musicname': cur,
        'author': re['author']
    }
    v += temp
    # find user according to name
    db.users.update_many({'name': user},{"$set": {"music_history": temp}})
    for i in db['users'].find():
        print(i)
    # user = User(name=request.json['name'], password=request.json['password']).save()
    return jsonify(re, "Success"), 201






if __name__ == "__main__":   
  
   # Get the database
   db = get_database()



    