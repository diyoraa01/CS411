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
print(db)
user1 = db.users

#begin code used for login
login_manager = flask_login.LoginManager()
login_manager.init_app(app)


@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"

def get_database():
    return client['Mx_world']




############



# create a new user after login with OAuth
@app.route('/create_user', methods=['POST'])
def create_user():
    re = request.json
    print(re['name'])
    db['users'].insert_one({
        
        'name': re['name'],
        'gender': re['gender'],
        'language': re['language'],
        'music_history': re['music_history']
        
    #    
    })
    
    # user = User(name=request.json['name'], password=request.json['password']).save()
    return jsonify(re), 201


# get the user information by (user name or user id)?
@app.route('/get_user', methods=['GET'])
def get_user():
    name = request.json

    return jsonify({'userinfo'}), 201




##########


# create a new music info after a user search a music
@app.route('/create_music', methods=['POST'])
def create_music():
    if not request.json or not 'name' in request.json or not 'password' in request.json:
        print("Wrong format of request in create_music: ", request)
        abort(400)
    re = request.json
    #user = re['user']
    db['music'].insert_one({
        'musicname': re['musicname'],
        'author': re['author']
    })
    
    # user = User(name=request.json['name'], password=request.json['password']).save()
    return jsonify({'userinfo in create_music'}), 201


# insert a music into user's music history
@app.route('/insert_music', methods=['POST'])
def insert_music():
    if not request.json or not 'name' in request.json or not 'password' in request.json:
        print("Wrong format of request in create_music: ", request)
        abort(400)
    re = request.json
    user = re['user']
    db['music'].insert_one({
        'musicname': re['musicname'],
        'author': re['author']
    })
    # find user according to name
    db.users.find({'name': "$user"})
    
    # user = User(name=request.json['name'], password=request.json['password']).save()
    return jsonify({'userinfo in insert_music'}), 201






if __name__ == "__main__":   
  
   # Get the database
   db = get_database()



    